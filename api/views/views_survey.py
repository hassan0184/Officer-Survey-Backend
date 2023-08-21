"""Survey Related ViewSets"""
import datetime
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView ,ListAPIView
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from rest_framework.permissions import IsAuthenticated
from officers_survey.pagination import CustomPagination
from api.serializers import (SurveySerializer, SurveyResponseSerializer,
DetailSurveyResponseSerializer, SurveyResponseForZipCodeSerializer,
CallBackSerializer)
from accounts.models import Officer
from survey.models import SurveyResponse, CallBack, CallBackNotes, QuestionResponse
from api.utils import (export_data_to_pdf, sucess_response,
not_found_error,date_format , send_request_change_email,
send_request_approved_email ,export_demographic_data_to_pdf)
from department.models import Department
from api.views.helper import get_survey_response
from api.utils import end_date_update

class SurveyViewSet(APIView):
    """Survey ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch Survey"""
        supervisor = Officer.objects.get(user=request.user)
        survey = SurveySerializer(supervisor.department.survey)
        return sucess_response(survey.data)

    def put(self, request):
        """Update Survey"""
        supervisor = Officer.objects.get(user=request.user)
        survey = supervisor.department.survey
        about = request.data.get("about")
        survey.about = about
        survey.save()
        survey = SurveySerializer(survey)
        return sucess_response(survey.data, 'Survey Updated Successfully')



class SurveyResponseViewSet(GenericAPIView):
    """Survey Response ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    def get(self, request):
        """Fetch Survey Response"""
        supervisor = Officer.objects.get(user=request.user)
        department_filter =  Q(officer__department=supervisor.department)
        data = get_survey_response(self, request, department_filter)
        if type(data) is Response:
            return data
        return Response(data)

class DetailSurveyResponseViewSet(APIView):
    """Detail Survey Response ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request, _pk):
        """Fetch Survey In Detail"""
        try:
            survey_response = SurveyResponse.objects.get(id=_pk)
            serializer = DetailSurveyResponseSerializer(survey_response)
            return sucess_response(serializer.data)
        except SurveyResponse.DoesNotExist:
            return not_found_error("Survey Not Found")

class SurveyResponseByOfficerViewSet(GenericAPIView):
    """Survey Response By Officer ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    def get(self, request, _pk):
        """Fetch Survey Response By Officer"""
        try:
            officer = Officer.objects.get(id=_pk)
            officer_search =  Q(officer=officer)
            data = get_survey_response(self, request, officer_search)
            if type(data) is Response:
                return data
            return Response(data)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")

class SurveyResponseByZipCodeViewSet(GenericAPIView):
    """Survey Response By ZipCode ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    def get(self, request):
        """Fetch Survey Response"""
        survey_filter = None
        zip_code = request.query_params.get("zip_code")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        supervisor = Officer.objects.get(user=request.user)
        survey_filter =  Q(officer__department=supervisor.department)
        if zip_code is not None:
            survey_filter  =  survey_filter & Q(zip_code=zip_code)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
            survey_filter  =  survey_filter & Q(created_at__gte=start_date)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request, end_date)
            survey_filter  =  survey_filter & Q(created_at__lte=end_date)
        survey_responses = SurveyResponse.objects.filter(survey_filter)
        query = SurveyResponse.objects.values('zip_code').filter(Q(survey_filter)).annotate(Avg('rating'), Count('rating'))
        graph_serializer = SurveyResponseForZipCodeSerializer(query, many=True)
        page = self.paginate_queryset(survey_responses)
        if page is not None:
            serializer = SurveyResponseSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = SurveyResponseSerializer(survey_responses, many=True)
            data = serializer.data
        data['zip_code_list'] = graph_serializer.data
        return Response(data)

class UpdateSurveyResponseBySupervisorViewSet(APIView):
    """"Update Survey Response By Supervisor ViewSet"""
    permission_classes = [IsAuthenticated]
    def put(self, request, _pk):
        """Update Survey Response"""
        try:
            survey_response = SurveyResponse.objects.get(id=_pk)
            rating = request.data.get("rating")
            change_reason = request.data.get("change_reason")
            survey_response.change_reason = change_reason
            survey_response.rating = rating
            supervisor = Officer.objects.get(user=request.user)
            survey_response.reviewed_by_supervisor = supervisor
            survey_response.changed_by_supervisor = True
            survey_response.save()
            serializer = DetailSurveyResponseSerializer(survey_response)
            return sucess_response(serializer.data, 'Review changed successfully')
        except SurveyResponse.DoesNotExist:
            return not_found_error("Survey Not Found")

class UpdateSurveyResponseByOfficerViewSet(APIView):
    """Update Survey Response ByOfficer ViewSet"""
    permission_classes = [IsAuthenticated]
    def put(self, request, _pk):
        """Update Survey Response"""
        try:
            survey_response = SurveyResponse.objects.get(id=_pk)
            officer = Officer.objects.get(user=request.user)
            comment_reason = request.data.get("comment_reason")
            survey_response.comment_reason = comment_reason
            survey_response.request_change = True
            survey_response.save()
            serializer = DetailSurveyResponseSerializer(survey_response)
            return sucess_response(serializer.data, "Change Request Submitted")
        except SurveyResponse.DoesNotExist:
            return not_found_error("Survey Not Found")


class GetSurveyResponseInPDF(APIView):
    """Get Survey Response In PDF"""
    def get(self, request, _pk):
        """Export Survey Response In PDF"""
        officer = Officer.objects.get(id=_pk)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        hours = request.query_params.get("hours", None)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request, end_date)
        return export_data_to_pdf(officer, start_date, end_date, hours)

class CallBackViewSet(ListAPIView):
    """Call Back ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = CallBackSerializer

    def get_queryset(self):
        supervisor = Officer.objects.get(user=self.request.user)
        return CallBack.objects.filter(survey__officer__department=supervisor.department).order_by('status')


class DetailCallBackViewSet(GenericAPIView):
    """Detail CallBack ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request, _pk):
        """Fetch Specific Call Back"""
        try:
            callback = CallBack.objects.get(id=_pk)
            serializer = CallBackSerializer(callback)
            return sucess_response(serializer.data)
        except CallBack.DoesNotExist:
            return not_found_error("Call Back Not Found")
    def put(self, request, _pk):
        """Update Specific CallBack """
        try:
            supervisor = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Supervisor Not Found")
        try:
            callback = CallBack.objects.get(id=_pk)
            status = request.data.get("status")
            callback.status = status
            notes = request.data.get("notes", '')
            callback.save()
            callback_note = CallBackNotes(
                reviewed_by_supervisor=supervisor,
                notes_by_supervivor=notes,
                callback=callback
            )
            callback_note.save()
            serializer = CallBackSerializer(callback)
            return sucess_response(serializer.data, 'Callback Updated')
        except CallBack.DoesNotExist:
            return not_found_error("Call Back Not Found")


class CallBackCountViewSet(GenericAPIView):
    """Call Back Count ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch Call Back Count"""
        try:
            supervisor = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Supervisor Not Found")
        try:
            call_backs = CallBack.objects.filter(survey__officer__department=supervisor.department, status="Requested")
            return sucess_response({'count': len(call_backs)})
        except CallBack.DoesNotExist:
            return not_found_error("Call Back Not Found")

class DemoGraphicResponseViewSet(GenericAPIView):
    """Demo Graphic Response ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """Fetch Count of Age, Race and Gender"""
        questions_filter = None
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        supervisor = Officer.objects.get(user=request.user)
        questions_filter =  Q(survey__officer__department=supervisor.department)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
            questions_filter  =  questions_filter & Q(survey__created_at__gte=start_date)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request, end_date)
            end_date = end_date + datetime.timedelta(days=1)
            questions_filter  =  questions_filter & Q(survey__created_at__lte=end_date)

        def get_question_count(question):
            """Get Questions Count"""
            data = QuestionResponse.objects.filter(question__question=question).filter(Q(questions_filter)).values('question__question').annotate(Count('question'))
            if data is not None and len(data) > 0:
                return data[0]['question__count']
            return 0

        age_count = list(QuestionResponse.objects.filter(question__question='What is your age group?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))
        race_count = list(QuestionResponse.objects.filter(question__question='What is your race?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))
        gender_count = list(QuestionResponse.objects.filter(question__question='What is your gender?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))

        age_question_count = get_question_count('What is your age group?')
        race_question_count = get_question_count('What is your race?')
        gender_question_count = get_question_count('What is your gender?')


        response_dict = {
            'demo_grpahic_response':{
                "age": {
                    "age_count": age_count,
                    "age_question_count": age_question_count,
                },
                "race": {
                    "race_count": race_count,
                    "race_question_count": race_question_count,
                },
                "gender": {
                    "gender_count": gender_count,
                    "gender_question_count": gender_question_count
                },
            }
        }
        return sucess_response(response_dict)

class DemoGraphicExportViewSet(APIView):
    """Demo Graphic Export ViewSet"""
    def get(self, request, _pk):
        """Export PDF Of Demo Graphic"""
        department = Department.objects.get(id=_pk)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        hours = request.query_params.get("hours", None)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request,end_date)
            end_date = end_date + datetime.timedelta(days=1)
        return export_demographic_data_to_pdf(department, start_date, end_date, hours)


class DemoGraphicResponseOfficerViewSet(GenericAPIView):
    """Demo Graphic Response ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """Fetch Count of Age, Race and Gender"""
        questions_filter = None
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        officer = Officer.objects.get(user=request.user)
        questions_filter =  Q(survey__officer=officer)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
            questions_filter  =  questions_filter & Q(survey__created_at__gte=start_date)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request, end_date)
            end_date = end_date + datetime.timedelta(days=1)
            questions_filter  =  questions_filter & Q(survey__created_at__lte=end_date)

        def get_question_count(question):
            """Get Questions Count"""
            data = QuestionResponse.objects.filter(question__question=question).filter(Q(questions_filter)).values('question__question').annotate(Count('question'))
            if data is not None and len(data) > 0:
                return data[0]['question__count']
            return 0

        age_count = list(QuestionResponse.objects.filter(question__question='What is your age group?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))
        race_count = list(QuestionResponse.objects.filter(question__question='What is your race?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))
        gender_count = list(QuestionResponse.objects.filter(question__question='What is your gender?').filter(Q(questions_filter)).values('choice__choice').annotate(Count('choice')))

        age_question_count = get_question_count('What is your age group?')
        race_question_count = get_question_count('What is your race?')
        gender_question_count = get_question_count('What is your gender?')


        response_dict = {
            'demo_grpahic_response':{
                "age": {
                    "age_count": age_count,
                    "age_question_count": age_question_count,
                },
                "race": {
                    "race_count": race_count,
                    "race_question_count": race_question_count,
                },
                "gender": {
                    "gender_count": gender_count,
                    "gender_question_count": gender_question_count
                },
            }
        }
        return sucess_response(response_dict)

class DemoGraphicExportOfficerViewSet(APIView):
    """Demo Graphic Export ViewSet"""
    def get(self, request, _pk):
        """Export PDF Of Demo Graphic"""
        officer = Officer.objects.get(id=_pk)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        hours = request.query_params.get("hours", None)
        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, date_format)
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, date_format)
            end_date = end_date_update(request,end_date)
            end_date = end_date + datetime.timedelta(days=1)
        return export_demographic_data_to_pdf(None, start_date, end_date, hours, officer)