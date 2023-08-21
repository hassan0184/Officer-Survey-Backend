"""Community Survey Related ViewSet"""
import uuid
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from officers_survey.pagination import CustomPagination
from accounts.models import Officer
from api.serializers import (CommunitySurveySerializer, CommunitySurveyResponseSerializer,
                             CommunitySurveyWithResponseCountSerializer, CommunitySurveyWithResponseSummarySerializer)
from api.utils import bad_request_error, sucess_response, not_found_error, export_community_data_to_pdf
from survey.models import (CommunitySurvey, CommunityQuestion,
                           CommunityChoice, CommunitySurveyResponse)


class CommunitySurveyViewSet(GenericAPIView):
    """Community Survey ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """Fetch Commuinty Survey Data"""

        category = request.GET.get('survery_category', None)
        officer = Officer.objects.get(user=request.user)

        survey_data = CommunitySurvey.objects.filter(department=officer.department).order_by('-created_at')

        if category:
            survey_data = survey_data.filter(survery_category=category)

        page = self.paginate_queryset(survey_data)
        if page is not None:
            serializer = CommunitySurveyWithResponseCountSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = CommunitySurveyWithResponseCountSerializer(survey_data, many=True)
            data = serializer.data
        return Response(data)

    def post(self, request):
        """Create Community Survey"""
        try:
            officer = Officer.objects.get(user=request.user)
            survey = None
            category = request.data.get("survery_category")
            title = request.data.get("title")
            survey_type = request.data.get("type", "Survey")
            instruction = request.data.get("instruction", "")
            expire = request.data.get("expire", None)
            if title is None or title == "":
                return not_found_error("Title Not Found")
            questions = request.data.get("questions", [])
            survey_model = CommunitySurvey(
                title=title,
                instruction=instruction,
                department=officer.department,
                link=uuid.uuid4().hex[:9].upper(),
                expire=expire,
                type=survey_type,
                survery_category=category,
            )
            survey_model.save()
            question_count = 1
            for question_data in questions:
                question = question_data.get("question")
                survey_type = question_data.get("type")
                required = question_data.get("required")
                choices = question_data.get("choices")
                if question is None or question == "":
                    return not_found_error("Question Not Found")
                if survey_type is None or survey_type == "":
                    return not_found_error("Type Not Found")
                if required is None:
                    return not_found_error("Required Not Found")
                question_model = CommunityQuestion(question=question, type=survey_type,
                                                   survey=survey_model, required=required, order=question_count)
                question_model.save()
                question_count = question_count + 1
                choice_count = 1
                for choice in choices:
                    if choice.get('choice') is None:
                        return not_found_error("Choice Not Found")
                    choice_model = CommunityChoice(
                        choice=choice.get('choice'),
                        question=question_model,
                        order=choice_count)
                    choice_count = choice_count + 1
                    choice_model.save()

            survey = CommunitySurveySerializer(survey_model)
            return sucess_response(survey.data, 'Survey Created Successfully')
        except Exception as e:
            return bad_request_error(message=str(e))


class DetailCommunitySurveyViewSet(APIView):
    """Detail Community Survey ViewSet"""
    permission_classes = [IsAuthenticated]

    def get(self, request, _pk):
        """Fetch Specific Community Survey"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        survey_data = CommunitySurvey.objects.get(department=officer.department, id=_pk)
        return sucess_response(CommunitySurveySerializer(survey_data).data)

    def put(self, request, _pk):
        """Update Survey"""
        officer = Officer.objects.get(user=request.user)
        survey_data = CommunitySurvey.objects.get(department=officer.department, id=_pk)
        title = request.data.get("title")
        instruction = request.data.get("instruction", "")
        expire = request.data.get("expire", None)
        delete_questions = request.data.get("delete_questions", [])
        survey_data.title = title
        survey_data.instruction = instruction
        survey_data.expire = expire
        questions = request.data.get("questions", [])
        question_count = 1
        for question_data in questions:
            question_id = question_data.get("id", None)
            question = question_data.get("question")
            question_type = question_data.get("type")
            required = question_data.get("required")
            choices = question_data.get("choices")
            delete_choices = question_data.get("delete_choices", [])
            if question is None or question == "":
                return not_found_error("Question Not Found")
            if question_type is None or question_type == "":
                return not_found_error("Type Not Found")
            if required is None:
                return not_found_error("Required Not Found")
            try:
                question_model = CommunityQuestion.objects.get(id=question_id)
                question_model.question = question
                question_model.type = question_type
                question_model.required = required
                question_model.order = question_count
            except:
                question_model = CommunityQuestion(question=question, type=question_type,
                                                   survey=survey_data, required=required, order=question_count)

            question_model.save()
            question_count = question_count + 1
            choice_count = 1
            for choice in choices:
                choice_id = choice.get("id", None)
                if choice.get('choice') is None:
                    return not_found_error("Choice Not Found")
                try:
                    choice_model = CommunityChoice.objects.get(id=choice_id)
                    choice_model.choice = choice.get('choice')
                    choice_model.order = choice_count
                except:
                    choice_model = CommunityChoice(
                        choice=choice.get('choice'),
                        question=question_model, order=choice_count)
                choice_model.save()
                choice_count = choice_count + 1
            for choice in delete_choices:
                try:
                    choice_model = CommunityChoice.objects.get(id=choice)
                    choice_model.delete()
                except CommunityChoice.DoesNotExist:
                    return not_found_error("Choice Not Found")
        for question in delete_questions:
            try:
                question_model = CommunityQuestion.objects.get(id=question)
                question_model.delete()
            except CommunityQuestion.DoesNotExist:
                return not_found_error("Question Not Found")
        survey_data.save()
        return sucess_response(CommunitySurveySerializer(survey_data).data, 'Survey Updated Successfully')

    def delete(self, request, _pk):
        """Delete Survey"""
        try:
            survey = CommunitySurvey.objects.get(id=_pk)
            survey.delete()
            return sucess_response(None, 'Survey Deleted  Successfully')
        except CommunitySurvey.DoesNotExist:
            return not_found_error('Survey Not Found')


class ExportCommunitySurveyViewSet(APIView):
    """Export Community Survey ViewSet"""

    def get(self, request, _pk):
        """Export Survey In PDF"""
        hours = request.query_params.get("hours", None)
        try:
            survey = CommunitySurvey.objects.get(id=_pk)
            return export_community_data_to_pdf(survey, hours)
        except CommunitySurvey.DoesNotExist:
            return not_found_error('Survey Not Found')


class CommunitySurveyResponseReportViewSet(APIView):
    """CommunitySurveyResponseReportViewSet"""
    permission_classes = [IsAuthenticated]

    def get(self, request, _pk):
        """Fetch Commuity Survey Response"""
        survey = CommunitySurvey.objects.get(id=_pk)
        return sucess_response(CommunitySurveyWithResponseSummarySerializer(survey, many=False).data, '')


class CommunitySurveyResponseViewSet(GenericAPIView):
    """Community Survey Response ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, _pk):
        """Fetch Response of Commuinty Survey"""
        try:
            survey = CommunitySurvey.objects.get(id=_pk)
            survey_data = CommunitySurveyResponse.objects.filter(survey=survey).order_by('-created_at')

            page = self.paginate_queryset(survey_data)
            if page is not None:
                serializer = CommunitySurveyResponseSerializer(page, many=True)
                result = self.get_paginated_response(serializer.data)
                data = result.data
            else:
                serializer = CommunitySurveyResponseSerializer(survey_data, many=True)
                data = serializer.data
            return Response(data)
        except CommunitySurvey.DoesNotExist:
            return not_found_error("Survey Not Found")


class CommunitySurveyReorderViewSet(APIView):
    """Community Survey Reorder ViewSet"""
    permission_classes = [IsAuthenticated]

    @classmethod
    def get_object(cls, _pk):
        """Get Community Survey"""
        try:
            survey = CommunitySurvey.objects.get(id=_pk)
            return survey
        except CommunitySurvey.DoesNotExist:
            return None

    def post(self, request, _pk):
        """Post Questions With Order Change"""
        survey = self.get_object(_pk)
        if survey is not None:
            try:
                questions = request.data.get("questions")
                count = 1
                for question in questions:
                    question_model = CommunityQuestion.objects.get(id=question)
                    question_model.order = count
                    count = count + 1
                    question_model.save()
                return sucess_response(None, 'Question Update Successfully')
            except CommunityQuestion.DoesNotExist:
                return not_found_error("Question Not Found")
        return not_found_error("Survey Not Found")
