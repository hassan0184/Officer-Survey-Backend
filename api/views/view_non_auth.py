"""Non Auth ViewSet"""
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from accounts.models import Officer
from api.serializers import (DepartmentWithSurveySerializer, DistrictSerializer,
OfficerSerializer,Employee360SurveySerializer,
Employee360SurveyResponseSerializer, CommunitySurveySerializer,
CommunitySurveyResponseSerializer, Employee360SurveyWithResponseSummarySerializer,
CommunitySurveyWithResponseSummarySerializer)
from api.utils import (sucess_response, not_found_error,
bad_request_error, send_demo_email, send_review_email,maximum_length_error, 
date_time_format)
from api.views.helper import add_officer
from department.models import Department, District
from survey.models import (Survey, SurveyResponse, Question,
Choice, QuestionResponse, CallBack, Employee360Survey,
Employee360QuestionResponse, Employee360Question, Employee360SurveyResponse,
Employee360Choice, CommunitySurvey, CommunityQuestionResponse,
CommunityQuestion, CommunitySurveyResponse, CommunityChoice)


class DeparmentViewSet(APIView):
    """Deparment ViewSet"""
    def get(self, request, _pk):
        """Fetch Department"""
        try:
            department = Department.objects.get(name=_pk)
            department = DepartmentWithSurveySerializer(department)
            return sucess_response(department.data)
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")

class DeparmentWithDistrictViewSet(APIView):
    """Deparment With District ViewSet"""
    def get(self, request, _pk):
        """Fetch Department's Districts"""
        try:
            department = Department.objects.get(link=_pk)
            districts = District.objects.filter(department=department)
            districts = DistrictSerializer(districts, many=True)
            department = DepartmentWithSurveySerializer(department)
            return sucess_response({
                'departent': department.data,
                'districts': districts.data,
            })
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")

class SerachOfficerInDeparmentViewSet(APIView):
    """Serach Officer In Deparment ViewSet"""
    def get(self, request, _pk):
        """Search Officer in Department"""
        try:
            department = Department.objects.get(id=_pk)
            search = request.query_params.get("search", "")
            officers = Officer.objects.filter(Q(department=department) & (
                Q(badge_number__istartswith=search) |
                Q(user__email__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search)
            ))
            officers = OfficerSerializer(officers, many=True)
            return sucess_response(officers.data)
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")


class SignupResponseViewSet(APIView):
    """Signup Response ViewSet"""
    def post(self, request, _pk):
        """Add Officer In The Specific Department"""
        try:
            department = Department.objects.get(id=_pk)
            officer = add_officer(request, department)
            if type(officer) is Officer:
                officer = OfficerSerializer(officer)
            else:
                return officer
            return sucess_response(officer.data, "Signup Completed. Kindly Login.")
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")


class AddSurveyResponseViewSet(APIView):
    """Add Survey Response ViewSet"""
    def post(self, request):
        """Add Survey"""
        officer = request.data.get("officer")
        survey = request.data.get("survey")
        citizen = request.data.get("citizen")
        questions_responses = request.data.get("questions_responses")
        rating = request.data.get("rating")
        comment = request.data.get("comment", '')
        if len(request.data.get("comment", "")) > 800:
            return maximum_length_error("Comment Is Greater Then Maximum Length") 
        comment = request.data.get("comment", '')
        try:
            officer = Officer.objects.get(id=officer)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        try:
            survey = Survey.objects.get(id=survey)
            if officer.department.survey.id != survey.id:
                return not_found_error("Provided survey is not found.")
        except survey.DoesNotExist:
            return not_found_error("Provided survey is not correct")
        first_name = citizen.get('first_name')
        last_name = citizen.get('last_name')
        address = citizen.get('address')
        phone = citizen.get('phone')
        city = citizen.get('city')
        state = citizen.get('state')
        zip_code = citizen.get('zip_code')
        if first_name is None:
            return not_found_error("Citizen First Name is reqiured")
        if last_name is None:
            return not_found_error("Citizen Last Name is reqiured")
        survey_response = SurveyResponse(
            officer=officer,
            survey=survey,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            comment=comment,
            rating=rating
        )
        survey_response.save()
        questions_responses_list = []
        for questions_response in questions_responses:
            question = questions_response.get('question')
            choice = questions_response.get('choice')
            comment_box = questions_response.get('comment')
            try:
                question = Question.objects.get(id=question)
                if officer.department.survey.id != question.survey.id:
                    survey_response.delete()
                    return not_found_error("Provided question is not of provided survey")
            except Question.DoesNotExist:
                survey_response.delete()
                return not_found_error("Provided Question is not correct")
            if question.type == 'Checkbox':
                choices = questions_response.get('choices')
                for choice in choices:
                    try:
                        choice = Choice.objects.get(id=choice)
                        questions_response_model = QuestionResponse(question=question,
                        survey=survey_response,choice=choice,comment_box=comment_box)
                        questions_responses_list.append(questions_response_model)
                        if officer.department.survey.id != choice.question.survey.id:
                            survey_response.delete()
                            return not_found_error("Provided choice is not of provided survey")
                    except Choice.DoesNotExist:
                        survey_response.delete()
                        return not_found_error("Provided choice is not correct")
            else:
                if choice is not None:
                    try:
                        choice = Choice.objects.get(id=choice)
                        if officer.department.survey.id != choice.question.survey.id:
                            survey_response.delete()
                            return not_found_error("Provided choice is not of provided survey")
                    except Choice.DoesNotExist:
                        survey_response.delete()
                        return not_found_error("Provided choice is not correct")
                if question.question == "Would you like a supervisor to call or email you about today’s situation?":
                    if choice.choice == 'Yes':
                        call_back = CallBack(
                            survey= survey_response,
                            comment=comment_box
                        )
                        call_back.save()
                questions_response_model = QuestionResponse(
                    question=question,
                    survey=survey_response,
                    choice=choice,
                    comment_box=comment_box
                )
                questions_responses_list.append(questions_response_model)

        for questions_response in questions_responses_list:
            questions_response.save()
        return sucess_response(None, 'Suucessfully added survey')


class RequestDemoViewSet(APIView):
    """Request Demo ViewSet"""
    def post(self, request):
        """Add Request Demo"""
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        department = request.data.get("department")
        job_title = request.data.get("job_title")
        work_email = request.data.get("work_email")
        phone = request.data.get("phone")
        try:
            send_demo_email(
                "Demo Request",
                "First Name :" + first_name + "\n" +
                "Last Name :" + last_name + "\n" +
                "Department :" + department + "\n" +
                "Job :" + job_title + "\n" +
                "Email :" + work_email + "\n" +
                "Phone :" + phone + "\n"
            )
            return sucess_response(None,
            'Your information has been submitted, we will contact you shortly.')
        except:
            bad_request_error("Email send failed! Try again later")


class Employee360SurveyByLinkViewSet(APIView):
    """Employee360 Survey By Link ViewSet"""
    def get(self, request, _pk):
        """Fetch Employee360 Link"""
        survey_data = Employee360Survey.objects.get(link=_pk)
        now = datetime.strptime(request.query_params.get("date"), date_time_format).timestamp()
        if survey_data.expire is not None:
            timediff =  survey_data.expire.timestamp() - now
            if timediff > 0:
                return sucess_response(Employee360SurveySerializer(survey_data).data, '')
            return not_found_error("Provided suvery is expired now")
        return sucess_response(Employee360SurveySerializer(survey_data).data, '')


class AddEmployee360SurveyRepsoneViewSet(APIView):
    """Add Employee360 Survey Repsone ViewSet"""
    def post(self, request):
        """Add Employee360Survey"""
        try:
            survey = request.data.get("survey")
            try:
                survey_model = Employee360Survey.objects.get(id=survey)
            except Employee360Survey.DoesNotExist:
                return not_found_error("Provided survey is not correct")
            survey_response = Employee360SurveyResponse(
                survey=survey_model
            )
            questions_responses_list = []
            questions = request.data.get("questions")
            for question_data in questions:
                question = question_data.get("question")
                choice = question_data.get("choice", None)
                rating = question_data.get("rating", None)
                file = question_data.get("file", None)
                if len(question_data.get("text", "")) > 800:
                    return maximum_length_error("Comment Is Greater Then Maximum Length") 
                text = question_data.get("text", "")
                if question is None:
                    return not_found_error("Question Not Found")
                try:
                    question_model = Employee360Question.objects.get(id=question)
                    if question_model.type == 'Checkbox':
                        choices = question_data.get("choices", None)
                        for choice in choices:
                            choice_model = Employee360Choice.objects.get(id=choice)
                            question_response_model = Employee360QuestionResponse(
                            question=question_model,choice=choice_model,comment_box=text,
                            survey=survey_response,rating=rating, file=file)
                            questions_responses_list.append(question_response_model)
                    else:
                        if choice is None:
                            question_response_model = Employee360QuestionResponse(
                            question=question_model,choice=None, comment_box=text,
                            survey=survey_response, rating=rating, file=file)
                        else:
                            choice_model = Employee360Choice.objects.get(id=choice)
                            question_response_model = Employee360QuestionResponse(
                            question=question_model,choice=choice_model, comment_box=text,
                            survey=survey_response, rating=rating, file=file)
                        questions_responses_list.append(question_response_model)
                except Employee360Question.DoesNotExist:
                    return not_found_error("Question Not Found")
            survey_response.save()
            for questions_response in questions_responses_list:
                questions_response.save()
            survey = Employee360SurveyResponseSerializer(survey_response)
            return sucess_response(Employee360SurveyWithResponseSummarySerializer(
            survey_model, many=False).data,'Survey Response Submitted Successfully')
        except:
            return bad_request_error("Something Went Wrong!")


class CommunitySurveyByLinkViewSet(APIView):
    """Community Survey By Link ViewSet"""
    def get(self, request, _pk):
        """Fetch Community Survey"""
        survey_data = CommunitySurvey.objects.get(link=_pk)
        now = datetime.strptime(request.query_params.get("date"), date_time_format).timestamp()
        if survey_data.expire is not None:
            timediff =  survey_data.expire.timestamp() - now
            if timediff > 0:
                return sucess_response(CommunitySurveySerializer(survey_data).data, '')
            return not_found_error("Provided suvery is expired now")
        return sucess_response(CommunitySurveySerializer(survey_data).data, '')

class AddCommunitySurveyRepsoneViewSet(APIView):
    """Add Community Survey Repsone ViewSet"""
    def post(self, request):
        """Add Community Survey"""
        try:
            survey = request.data.get("survey")
            try:
                survey_model = CommunitySurvey.objects.get(id=survey)
            except CommunitySurvey.DoesNotExist:
                return not_found_error("Provided survey is not correct")
            survey_response = CommunitySurveyResponse(
                survey=survey_model
            )

            questions_responses_list = []
            questions = request.data.get("questions")
            for question_data in questions:
                question = question_data.get("question")
                choice = question_data.get("choice", None)
                if len(question_data.get("text", "")) > 800:
                    return maximum_length_error("Comment Is Greater Then Maximum Length") 
                text = question_data.get("text", "")
                rating = question_data.get("rating", None)
                file = question_data.get("file", None)
                if question is None:
                    return not_found_error("Question Not Found")
                try:
                    question_model = CommunityQuestion.objects.get(id=question)
                    if question_model.type == 'Checkbox':
                        choices = question_data.get("choices", None)
                        for choice in choices:
                            choice_model = CommunityChoice.objects.get(id=choice)
                            question_response_model = CommunityQuestionResponse(
                            question=question_model,choice=choice_model, comment_box=text,
                            survey=survey_response, rating=rating, file=file)
                            questions_responses_list.append(question_response_model)
                    else:
                        if choice is None:
                            question_response_model = CommunityQuestionResponse(
                            question=question_model,choice=None, comment_box=text,
                            survey=survey_response, rating=rating, file=file)
                        else:
                            choice_model = CommunityChoice.objects.get(id=choice)
                            question_response_model = CommunityQuestionResponse(
                            question=question_model, choice=choice_model, comment_box=text,
                            survey=survey_response, rating=rating, file=file)
                        questions_responses_list.append(question_response_model)
                except CommunityQuestion.DoesNotExist:
                    return not_found_error("Question Not Found")
            survey_response.save()
            for questions_response in questions_responses_list:
                questions_response.save()
            survey = CommunitySurveyResponseSerializer(survey_response)
            return sucess_response(CommunitySurveyWithResponseSummarySerializer(
            survey_model, many=False).data,'Survey Response Submitted Successfully')
        except:
            return bad_request_error("Something Went Wrong!")
