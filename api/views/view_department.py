"""Department Related ViewSets"""
import datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Avg
from api.serializers import DepartmentSerializer, OfficerSerializer, DetailOfficerSerializer
from api.utils import not_found_error, sucess_response, send_issue_email
from accounts.models import Officer, Log
from department.models import Support
from survey.models import SurveyResponse

class UpdateDepartmentViewSet(APIView):
    """Update Department ViewSet"""
    permission_classes = [IsAuthenticated]
    def put(self, request):
        """Upadte Department"""
        officer = Officer.objects.get(user=request.user)
        no_of_days = request.data.get("no_of_days", 0)
        trigger_rating = request.data.get("trigger_rating", 0)
        department = officer.department
        if no_of_days is not None:
            department.no_of_days = no_of_days
        if trigger_rating is not None:
            department.trigger_rating = trigger_rating
        department.save()
        return sucess_response(DepartmentSerializer(department).data, 'Trigger Setting Updated')

    def get(self, request):
        """Fetch Department of a Officer"""
        officer = Officer.objects.get(user=request.user)
        return sucess_response(DepartmentSerializer(officer.department).data)

class OfficerNeedTrainingViewSet(APIView):
    """Officer Need Training ViewSet"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch Officers of Department"""
        officer = Officer.objects.get(user=request.user)
        department = officer.department
        trigger_end_date = datetime.datetime.now()
        trigger_start_date = trigger_end_date - datetime.timedelta(days=department.no_of_days)
        filter_response1  =  Q(created_at__gte=trigger_start_date)
        filter_response2  =  filter_response1 & Q(created_at__lte=trigger_end_date)
        filter_response3  =  filter_response2 & Q(officer__department=department)
        filter_response4  =  filter_response3 & Q(officer__training=False)
        officers = SurveyResponse.objects.values('officer').filter(filter_response4).annotate(Avg('rating')).filter(Q(rating__avg__lte=department.trigger_rating))
        officera_data = []
        for officer in officers:
            logs = Log.objects.filter(officer__id=officer.get('officer')).order_by('-created_at')
            if len(logs) > 0:
                log = logs[0]
                if log.in_training is False:
                    delta = datetime.datetime.now() - log.created_at.replace(tzinfo=None)
                    days = delta.days
                    if days>= department.no_of_days:
                        officera_data.append(Officer.objects.get(id=officer.get('officer')))
            else:
                officera_data.append(Officer.objects.get(id=officer.get('officer')))
        officers = OfficerSerializer(officera_data, many=True)
        return sucess_response(officers.data)

    def put(self, request, _pk):
        """Update Officer Who Is Moved to Training"""
        try:
            supervisor = Officer.objects.get(user=request.user)
            officer = Officer.objects.get(id=_pk)
            officer.training = True
            officer.save()
            log = Log(
                officer=officer,
                in_training=True,
                supervisor=supervisor
            )
            log.save()
            return sucess_response(None, 'Officer Moved to training')
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")

class OfficerInTrainingViewSet(APIView):
    """Officer In TrainingViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch Officers Who Were Involved In Training"""
        officer = Officer.objects.get(user=request.user)
        department = officer.department
        filter_response1  =  Q(training=True)
        filter_response2  =  filter_response1 & Q(department=department)
        officers = Officer.objects.filter(filter_response2)
        officers = DetailOfficerSerializer(officers, many=True)
        return sucess_response(officers.data)

    def put(self, request, _pk):
        """Update Officer Who Is Moved Out of Training"""
        try:
            supervisor = Officer.objects.get(user=request.user)
            officer = Officer.objects.get(id=_pk)
            officer.training = False
            officer.save()
            log = Log(
                officer=officer,
                in_training=False,
                supervisor=supervisor
            )
            log.save()
            return sucess_response(None, 'Officer Moved out of training')
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")


class SupportViewSet(APIView):
    """Support ViewSet"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """Create Support for Officer of a Department"""
        officer = Officer.objects.get(user=request.user)
        issue = request.data.get("issue")
        message = request.data.get("message")
        picture = request.data.get("picture")
        support = Support(
            title=issue,
            description=message,
            pic=picture
        )
        support.user = officer
        support.save()
        if support.pic is None:
            send_issue_email(
                "Tech Support",
                "Department: " + officer.department.name  +
                "\nEmail: " +  request.user.email + "\nIssue: " +
                support.title + "\nMessage: " + support.description
            )
        else:
            send_issue_email(
                "Tech Support",
                "Department: " + officer.department.name  +
                "\nEmail: " +  request.user.email + "\nIssue: " +
                support.title + "\nMessage: " + support.description
                + "\nImage: " + support.pic.url
            )
        return sucess_response(None, 'Thanks! We will be in touch very soon.')

class UpdateDepartmentDescriptionViewSet(APIView):
    """Update Department Description ViewSet"""
    permission_classes = [IsAuthenticated]
    def put(self, request):
        """Update Department Description"""
        officer = Officer.objects.get(user=request.user)
        department = officer.department
        header = request.data.get("header")
        department.header = header
        department.save()
        return sucess_response(DepartmentSerializer(department).data, 'Successfully Updated')
