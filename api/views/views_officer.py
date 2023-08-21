"""Officers Related ViewSet"""
import os
from decouple import config
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.serializers import LogSerializer, OfficerSerializer, DetailOfficerSerializer, OfficerSurveyDetailSerializer
from accounts.models import Officer, Log
from api.utils import (not_found_error, sucess_response,
                       handle_uploaded_file, bad_request_error, send_account_created_email)
from api.views.helper import add_officer, update_officer
import base64
import xlsxwriter
import boto3
from botocore.client import Config


class ListOfficersCSV(APIView):
    """List Officers ViewSet"""
    permission_classes = [AllowAny]

    def post(self, request):
        """List Officer On csv file"""
        file_name = 'Officers.xlsx'
        image = 'image_to_save'
        ext = '.png'

        officer_ = Officer.objects.filter(
            first_name=request.data[0]['FirstName'], badge_number=request.data[0]['Badge']).first()

        if officer_:
            file_name = officer_.department.name + "_" + file_name

        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'FirstName')
        worksheet.write('B1', 'LastName')
        worksheet.write('C1', 'Badge')
        worksheet.write('D1', 'QRCode')

        # set width size of cell 4
        worksheet.set_column('D:D', 22)
        # set height of all cells
        worksheet.set_default_row(150)
        row = 1
        total = len(request.data)

        for i in range(0, total):
            image_paste = True
            try:
                res = bytes(request.data[i]["qr"], 'utf-8')
                with open(image+str(i)+ext, "wb") as fh:
                    fh.write(base64.decodebytes(res))
                fh.close()
            except Exception as e:
                image_paste = False
                print(e)
            column = 0
            for key in request.data[i]:
                if key == 'qr':
                    if image_paste:
                        worksheet.insert_image(row, column, image+str(i)+ext,
                                               {'x_scale': 0.8, 'y_scale': 0.8})
                else:
                    worksheet.write(row, column, request.data[i][key])
                column += 1
            row += 1
        workbook.close()

        try:
            session = boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            )
            s3 = session.client('s3', config=Config(signature_version='s3v4'))
            with open(file_name, "rb") as f:
                s3.upload_fileobj(f, 'officer-survey-qr-export', file_name,
                                  ExtraArgs={'ACL': 'public-read'})

            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'officer-survey-qr-export',
                    'Key': file_name
                }
            )
        except Exception as e:
            return bad_request_error("error uploading file"+str(e))

        try:
            for i in range(0, total):
                os.remove(image+str(i)+ext)
            os.remove(file_name)
        except Exception as e:
            print(e)

        url = str(url).split("?")
        return sucess_response(url[0], 'Officer CSV created Successfully!')


class ListOfficersViewSet(APIView):
    """List Officers ViewSet"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List Officer On Related Search"""
        search = request.query_params.get("search", "")
        supervisor = Officer.objects.get(user=request.user)
        officers = Officer.objects.filter(
            Q(department=supervisor.department) &
            (
                Q(badge_number__istartswith=search) |
                Q(user__email__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search)
            ))
        officers = OfficerSerializer(officers, many=True)
        return sucess_response(officers.data)

    def delete(self, request, _pk):
        """Delete Officer"""
        officer = Officer.objects.get(user=request.user)
        try:
            officer = Officer.objects.get(id=_pk)
            officer.user.delete()
            officer.delete()
            return sucess_response(None, 'Deleted Officer Successfully')
        except Officer.DoesNotExist:
            return not_found_error('Officer Not Found')

    def post(self, request):
        """Add Officer"""
        supervisor = Officer.objects.get(user=request.user)
        officer = add_officer(request, supervisor.department)
        if type(officer) is Officer:
            serializer = OfficerSerializer(officer)
        else:
            return officer
        password = request.data.get("password")
        base_link = None
        if os.environ.get('BASE_URL') is None:
            base_link = config('BASE_URL')
        else:
            base_link = os.environ['BASE_URL']
        send_account_created_email("Account Created",
                                   "Your Officer Survey account has been created. To complete your registration process you must login and change your password. \n\nEmail : " + officer.user.email + "\nPassword : " + password + "\n\nClick here to login " + base_link + "/login \n\nIf you have questions or need help, please contact the appropriate personnel in your department. \n\nThis message was sent from an automated system that cannot receive emails. Please do not reply to this message", officer.user.email)
        return sucess_response(serializer.data, 'Officer Added Successfully!')

    def put(self, request, _pk):
        """Update Officer"""
        try:
            supervisor = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Supervisor Not Found")
        officer = None
        try:
            officer = Officer.objects.get(id=_pk)
        except Officer.DoesNotExist:
            return not_found_error('Officer Not found')
        officer = update_officer(request, officer)
        if type(officer) is Officer:
            officer = OfficerSerializer(officer)
        else:
            return officer
        return sucess_response(officer.data, 'Officer Updated Successfully!')


class DetailOfficersViewSet(APIView):
    """Detail Officers ViewSet"""
    permission_classes = [IsAuthenticated]

    def get(self, request,  _pk):
        """List Detail Officers"""
        try:
            officer = Officer.objects.get(id=_pk)
            officers = DetailOfficerSerializer(officer)
            return sucess_response(officers.data)
        except Officer.DoesNotExist:
            return not_found_error('Officer Not Found')


class DetailOfficersSurveyViewSet(APIView):
    """Detail Officers ViewSet for officer survey"""
    permission_classes = [AllowAny]

    def get(self, request,  link):
        """List Detail Officers"""

        officer = Officer.objects.filter(link=link).first()

        if officer is None:
            return not_found_error('Officer Not Found')

        officers = OfficerSurveyDetailSerializer(officer)
        return sucess_response(officers.data)


class UploadOfficersViewSet(APIView):
    """Upload Officers ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Officers Added In File"""
        try:
            if len(request.FILES) != 0:
                file = request.FILES['file']
            else:
                return bad_request_error("required a csv/xlsx file as input")
            message = handle_uploaded_file(request, file)
            if message != "":
                return bad_request_error(message)
            return sucess_response(None, 'All Officer Added Successfully')
        except Exception as e:
            return bad_request_error(e)


class UpdateOfficerPasswordViewSet(APIView):
    """Update Officer Password ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Update Password Of Officer"""
        officer = Officer.objects.get(user=request.user)
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        user = authenticate(username=officer.user.email, password=password)
        if user is not None:
            user.password = make_password(new_password)
            user.save()
            return sucess_response(None, 'Password Updated Successfully')
        return bad_request_error("Password Not Correct")


class OfficerLogViewSet(APIView):
    """Officer LogView Set"""
    permission_classes = [IsAuthenticated]

    def get(self, request, _pk):
        """Fetch Logged Officer"""
        try:
            officer = Officer.objects.get(id=_pk)
            logs = Log.objects.filter(officer=officer)
            logs = LogSerializer(logs, many=True)
            return sucess_response(logs.data)
        except Officer.DoesNotExist:
            return not_found_error('Officer Not Found')
