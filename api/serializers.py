"""Serializers Related to User, Department and Survey"""
import os
from decouple import config
from rest_framework import serializers
from django.db.models import Count
from accounts.models import Officer, User, Log, Notes
from department.models import District, Department
from survey.models import (Survey, Question, Choice, SurveyResponse,
                           QuestionResponse, CallBack, CallBackNotes, QuestionTranslation,
                           ChoiceTranslation, Employee360Survey, Employee360Question,
                           Employee360Choice, Employee360SurveyResponse, Employee360QuestionResponse,
                           CommunitySurvey, CommunityQuestion, CommunityChoice, CommunitySurveyResponse,
                           CommunityQuestionResponse)

from events.models import SmsSurvey, EventTypes, MessageSendData
from miscellaneous.models import LatitudeLongitude
from api.utils import date_time_format, get_lat_long


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = User
        fields = ['email', 'profile_pic', 'is_superuser']


class DistrictSerializer(serializers.ModelSerializer):
    """District Serializer"""
    class Meta:
        model = District
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    """Department Serializer"""
    sign_up_link = serializers.SerializerMethodField()

    @classmethod
    def get_sign_up_link(cls, obj):
        """get signup link"""
        base_link = None
        if os.environ.get('BASE_URL') is None:
            base_link = config('BASE_URL')
        else:
            base_link = os.environ['BASE_URL']
        return base_link + "/signupofficer/" + obj.link

    class Meta:
        model = Department
        fields = '__all__'


class OfficerSerializer(serializers.ModelSerializer):
    """Officer Serializer"""
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Officer
        fields = '__all__'


class DetailOfficerSerializer(serializers.ModelSerializer):
    """Detail Officer Serializer"""
    user = UserSerializer(many=False, read_only=True)
    district = DistrictSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Officer
        fields = '__all__'


class QuestionTranslationSerializer(serializers.ModelSerializer):
    """Question TranslationSerializer """
    class Meta:
        model = QuestionTranslation
        fields = '__all__'


class ChoiceTranslationSerializer(serializers.ModelSerializer):
    """Choice Translation Serializer"""
    class Meta:
        model = ChoiceTranslation
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""
    choice_translations = serializers.SerializerMethodField()

    @classmethod
    def get_choice_translations(cls, obj):
        """get choice translations"""
        return ChoiceTranslationSerializer(ChoiceTranslation.objects.filter(choice=obj),
                                           many=True).data

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Question Serializer"""
    choices = ChoiceSerializer(many=True)
    question_translations = serializers.SerializerMethodField()

    @classmethod
    def get_question_translations(cls, obj):
        """get question translation"""
        return QuestionTranslationSerializer(QuestionTranslation.objects.filter(question=obj),
                                             many=True).data

    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    """Survey Serializer"""
    questions = serializers.SerializerMethodField()

    @classmethod
    def get_questions(cls, obj):
        """get questions in order"""
        return QuestionSerializer(Question.objects.filter(survey=obj).order_by('order'),
                                  many=True).data

    class Meta:
        model = Survey
        fields = '__all__'


class QuestionSerializerForResponse(serializers.ModelSerializer):
    """Question Serializer For Response"""
    class Meta:
        model = Question
        fields = '__all__'


class QuestionResponseSerializer(serializers.ModelSerializer):
    """Question Response Serializer"""
    question = QuestionSerializerForResponse(many=False, read_only=True)
    choice = ChoiceSerializer(many=False, read_only=True)
    check_box_answers = serializers.SerializerMethodField()

    @classmethod
    def get_check_box_answers(cls, obj):
        """get checkbox answers"""
        if obj.question.type == 'Checkbox':
            response = QuestionResponse.objects.filter(
                question=obj.question, survey=obj.survey)
            string = ""
            for index, item in enumerate(response):
                string = string + item.choice.choice
                if index < len(response) - 1:
                    string = string + ", "
            return string
        return ""

    class Meta:
        model = QuestionResponse
        fields = ['question', 'choice', 'comment_box', 'check_box_answers']


class SurveyResponseSerializer(serializers.ModelSerializer):
    """Survey Response Serializer"""
    officer = OfficerSerializer(many=False, read_only=True)

    class Meta:
        model = SurveyResponse
        fields = '__all__'


class DetailSurveyResponseSerializer(serializers.ModelSerializer):
    """Detail Survey Response Serializer"""
    officer = DetailOfficerSerializer(many=False, read_only=True)
    reviewed_by_supervisor = DetailOfficerSerializer(
        many=False, read_only=True)
    questions_response = serializers.SerializerMethodField()

    @classmethod
    def get_questions_response(cls, obj):
        """get questions response"""
        question_ids = QuestionResponse.objects.filter(survey=obj).order_by(
            'question__order').values('question__id').distinct()
        data = []
        for question in question_ids:
            data.append(QuestionResponse.objects.filter(survey=obj,
                                                        question__id=question['question__id']).first())
        return QuestionResponseSerializer(data, many=True).data

    class Meta:
        model = SurveyResponse
        fields = '__all__'


class SurveyResponseForGraphSerializer(serializers.ModelSerializer):
    """Survey Response For GraphSerializer"""
    created_at__date = serializers.DateField(format=date_time_format)
    rating__avg = serializers.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        model = SurveyResponse
        fields = ['created_at__date', 'rating__avg']


class SurveyResponseForZipCodeSerializer(serializers.ModelSerializer):
    """Survey Response For ZipCodeSerializer"""
    rating__avg = serializers.DecimalField(decimal_places=2, max_digits=5)
    zip_code = serializers.CharField()
    rating__count = serializers.IntegerField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    @classmethod
    def get_latitude(cls, obj):
        """get latitude value of zip_code"""
        latitude = LatitudeLongitude.objects.filter(
            zip_code=obj.get('zip_code'))
        if latitude.count() == 0:
            get_latitude = get_lat_long(obj.get('zip_code'))
            if get_latitude.get('lat') is not None:
                location = LatitudeLongitude(latitude=get_latitude.get(
                    'lat'), longitude=get_latitude.get('lng'), zip_code=obj.get('zip_code'))
                location.save()
                return get_latitude.get('lat')
            return get_latitude.get('lat')
        res = latitude.first()
        return res.latitude

    @classmethod
    def get_longitude(cls, obj):
        """get longitude value of zip_code"""
        longitude = LatitudeLongitude.objects.filter(
            zip_code=obj.get('zip_code'))
        if longitude.count() == 0:
            return get_lat_long(obj.get('zip_code')).get('lng')
        res = longitude.first()
        return res.longitude

    class Meta:
        model = SurveyResponse
        fields = ['zip_code', 'rating__avg',
                  'latitude', 'longitude', 'rating__count']


class DepartmentWithSurveySerializer(serializers.ModelSerializer):
    """Department With SurveySerializer"""
    survey = SurveySerializer(many=False, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class OfficerNeedTrainingSerializer(serializers.ModelSerializer):
    """Officer Need Training Serializer"""
    officer = serializers.SerializerMethodField()

    @classmethod
    def get_officer(cls, obj):
        """get specific officer"""
        return OfficerSerializer(Officer.objects.get(id=obj.get('officer'))).data

    class Meta:
        model = SurveyResponse
        fields = ['officer']


class LogSerializer(serializers.ModelSerializer):
    """Log Serializer"""
    officer = DetailOfficerSerializer(many=False, read_only=True)
    supervisor = DetailOfficerSerializer(many=False, read_only=True)

    class Meta:
        model = Log
        fields = '__all__'


class CallBackNotesSerializer(serializers.ModelSerializer):
    """CallBack Notes Serializer"""
    reviewed_by_supervisor = DetailOfficerSerializer(
        many=False, read_only=True)

    class Meta:
        model = CallBackNotes
        fields = ('notes_by_supervivor', 'reviewed_by_supervisor',)


class CallBackSerializer(serializers.ModelSerializer):
    """CallBack Serializer"""
    survey = DetailSurveyResponseSerializer(many=False, read_only=True)
    notes = serializers.SerializerMethodField()

    @classmethod
    def get_notes(cls, obj):
        """get callback notes"""
        return CallBackNotesSerializer(CallBackNotes.objects.filter(callback=obj),
                                       many=True).data

    class Meta:
        model = CallBack
        fields = ('id', 'survey', 'comment', 'status', 'notes',)


class NotesSerializer(serializers.ModelSerializer):
    """Notes Serializer"""
    notes_by = DetailOfficerSerializer(many=False, read_only=True)
    notes_for = DetailOfficerSerializer(many=False, read_only=True)

    class Meta:
        model = Notes
        fields = '__all__'


class Employee360ChoiceSerializer(serializers.ModelSerializer):
    """Employee360 Choice Serializer"""
    class Meta:
        model = Employee360Choice
        fields = '__all__'


class Employee360QuestionSerializer(serializers.ModelSerializer):
    """Employee360 Question Serializer"""
    choices = Employee360ChoiceSerializer(many=True)

    class Meta:
        model = Employee360Question
        fields = '__all__'


class Employee360SurveySerializer(serializers.ModelSerializer):
    """Employee360 Survey Serializer"""
    questions = serializers.SerializerMethodField()

    @classmethod
    def get_questions(cls, obj):
        """get questions"""
        return Employee360QuestionSerializer(Employee360Question.objects.filter(survey=obj).order_by('order'),
                                             many=True).data

    class Meta:
        model = Employee360Survey
        fields = '__all__'


class Employee360QuestionResponseSerializer(serializers.ModelSerializer):
    """Employee360 Question Response Serializer"""
    question = Employee360QuestionSerializer(many=False, read_only=True)
    choice = Employee360ChoiceSerializer(many=False, read_only=True)
    check_box_answers = serializers.SerializerMethodField()

    @classmethod
    def get_check_box_answers(cls, obj):
        """get check box answers"""
        if obj.question.type == 'Checkbox':
            response = Employee360QuestionResponse.objects.filter(question=obj.question,
                                                                  survey=obj.survey)
            string = ""
            for index, item in enumerate(response):
                string = string + item.choice.choice
                if index < len(response) - 1:
                    string = string + ", "
            return string
        return ""

    class Meta:
        model = Employee360QuestionResponse
        fields = ['choice', 'check_box_answers',
                  'question', 'rating', 'file', 'comment_box', 'id']


class Employee360SurveyResponseSerializer(serializers.ModelSerializer):
    """Employee360 Survey Response Serializer"""
    questions_response = serializers.SerializerMethodField()

    @classmethod
    def get_questions_response(cls, obj):
        """get questions response"""
        question_ids = Employee360QuestionResponse.objects.filter(
            survey=obj).order_by('question__order').values('question__id').distinct()
        data = []
        for question in question_ids:
            data.append(Employee360QuestionResponse.objects.filter(survey=obj,
                                                                   question__id=question['question__id']).first())
        return Employee360QuestionResponseSerializer(data, many=True).data

    class Meta:
        model = Employee360SurveyResponse
        fields = '__all__'


class Employee360SurveyWithResponseCountSerializer(serializers.ModelSerializer):
    """Employee360 Survey With Response Count Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of survey"""
        data = Employee360SurveyResponse.objects.values(
            'survey__id').filter(survey=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    class Meta:
        model = Employee360Survey
        fields = ['id', 'title', 'link', 'count', 'expire', 'type', 'survery_category']


class Employee360ChoiceResponseSummarySerializer(serializers.ModelSerializer):
    """Employee360 Choice Response Summary Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of choices"""
        data = Employee360QuestionResponse.objects.values(
            'choice__id').filter(choice=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    class Meta:
        model = Employee360Choice
        fields = ['id', 'choice', 'count']


class Employee360QuestionResponseSummarySerializer(serializers.ModelSerializer):
    """Employee360 Question Response Summary Serializer"""
    choices = Employee360ChoiceResponseSummarySerializer(many=True)
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of questions"""
        data = Employee360QuestionResponse.objects.values(
            'question__id').filter(question=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    text_responses = serializers.SerializerMethodField()

    @classmethod
    def get_text_responses(cls, obj):
        """get text responses"""
        data = Employee360QuestionResponse.objects.filter(question=obj,
                                                          question__type="Text Area")
        arr = []
        for survey in data:
            arr.append(survey.comment_box)
        return arr

    file_responses = serializers.SerializerMethodField()

    @classmethod
    def get_file_responses(cls, obj):
        """get file responses"""
        data = Employee360QuestionResponse.objects.filter(
            question=obj, question__type="File")
        arr = []
        for survey in data:
            arr.append(survey.file)
        return arr

    ratings = serializers.SerializerMethodField()

    @classmethod
    def get_ratings(cls, obj):
        """get ratings of employee360 question response"""
        response1 = Employee360QuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                      question__type="Rating", rating=1).annotate(Count('rating'))
        response2 = Employee360QuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                      question__type="Rating", rating=2).annotate(Count('rating'))
        response3 = Employee360QuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                      question__type="Rating", rating=3).annotate(Count('rating'))
        response4 = Employee360QuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                      question__type="Rating", rating=4).annotate(Count('rating'))
        response5 = Employee360QuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                      question__type="Rating", rating=5).annotate(Count('rating'))
        data = []
        if response1 is not None and len(response1) > 0:
            data.append(response1[0]['rating__count'])
        else:
            data.append(0)
        if response2 is not None and len(response2) > 0:
            data.append(response2[0]['rating__count'])
        else:
            data.append(0)
        if response3 is not None and len(response3) > 0:
            data.append(response3[0]['rating__count'])
        else:
            data.append(0)
        if response4 is not None and len(response4) > 0:
            data.append(response4[0]['rating__count'])
        else:
            data.append(0)
        if response5 is not None and len(response5) > 0:
            data.append(response5[0]['rating__count'])
        else:
            data.append(0)

        return data

    class Meta:
        model = Employee360Question
        fields = ['id', 'question', 'choices', 'count', 'type',
                  'text_responses', 'ratings', 'file_responses']


class Employee360SurveyWithResponseSummarySerializer(serializers.ModelSerializer):
    """Employee360 Survey With Response Summary Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of survey"""
        data = Employee360SurveyResponse.objects.values(
            'survey__id').filter(survey=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    questions = serializers.SerializerMethodField()

    @classmethod
    def get_questions(cls, obj):
        """get questions in order"""
        return Employee360QuestionResponseSummarySerializer(Employee360Question.objects.filter(survey=obj).order_by('order'),
                                                            many=True).data

    class Meta:
        model = Employee360Survey
        fields = ['id', 'title', 'link', 'count', 'questions']


class CommunityChoiceSerializer(serializers.ModelSerializer):
    """Community Choice Serializer"""
    class Meta:
        model = CommunityChoice
        fields = '__all__'


class CommunityQuestionSerializer(serializers.ModelSerializer):
    """Community Question Serializer"""
    choices = CommunityChoiceSerializer(many=True)

    class Meta:
        model = CommunityQuestion
        fields = '__all__'


class CommunitySurveySerializer(serializers.ModelSerializer):
    """Community Survey Serializer"""
    questions = serializers.SerializerMethodField()

    @classmethod
    def get_questions(cls, obj):
        """get questions in order"""
        return CommunityQuestionSerializer(CommunityQuestion.objects.filter(survey=obj).order_by('order'),
                                           many=True).data

    class Meta:
        model = CommunitySurvey
        fields = '__all__'


class CommunityQuestionResponseSerializer(serializers.ModelSerializer):
    """Community Question Response Serializer"""
    question = CommunityQuestionSerializer(many=False, read_only=True)
    choice = CommunityChoiceSerializer(many=False, read_only=True)

    check_box_answers = serializers.SerializerMethodField()

    @classmethod
    def get_check_box_answers(cls, obj):
        """get check box answers"""
        if obj.question.type == 'Checkbox':
            response = CommunityQuestionResponse.objects.filter(question=obj.question,
                                                                survey=obj.survey)
            string = ""
            for index, item in enumerate(response):
                string = string + item.choice.choice
                if index < len(response) - 1:
                    string = string + ", "
            return string
        return ""

    class Meta:
        model = CommunityQuestionResponse
        fields = ['choice', 'check_box_answers', 'question',
                  'rating', 'file', 'comment_box', 'id']


class CommunitySurveyResponseSerializer(serializers.ModelSerializer):
    """Community Survey Response Serializer"""
    questions_response = serializers.SerializerMethodField()

    @classmethod
    def get_questions_response(cls, obj):
        """get questions response"""
        question_ids = CommunityQuestionResponse.objects.filter(
            survey=obj).order_by('question__order').values('question__id').distinct()
        data = []
        for question in question_ids:
            data.append(CommunityQuestionResponse.objects.filter(survey=obj,
                                                                 question__id=question['question__id']).first())
        return CommunityQuestionResponseSerializer(data, many=True).data

    class Meta:
        model = CommunitySurveyResponse
        fields = '__all__'


class CommunitySurveyWithResponseCountSerializer(serializers.ModelSerializer):
    """Community Survey With Response Count Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of survey"""
        data = CommunitySurveyResponse.objects.values(
            'survey__id').filter(survey=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    class Meta:
        model = CommunitySurvey
        fields = ['id', 'title', 'link', 'count', 'expire', 'type', 'survery_category']


class CommunityChoiceResponseSummarySerializer(serializers.ModelSerializer):
    """Community Choice Response Summary Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get choices count"""
        data = CommunityQuestionResponse.objects.values(
            'choice__id').filter(choice=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    class Meta:
        model = CommunityChoice
        fields = ['id', 'choice', 'count']


class CommunityQuestionResponseSummarySerializer(serializers.ModelSerializer):
    """Community Question Response Summary Serializer"""
    choices = CommunityChoiceResponseSummarySerializer(many=True)
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of questions"""
        data = CommunityQuestionResponse.objects.values(
            'question__id').filter(question=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    text_responses = serializers.SerializerMethodField()

    @classmethod
    def get_text_responses(cls, obj):
        """get text responses"""
        data = CommunityQuestionResponse.objects.filter(
            question=obj, question__type="Text Area")
        arr = []
        for survey in data:
            arr.append(survey.comment_box)
        return arr

    file_responses = serializers.SerializerMethodField()

    @classmethod
    def get_file_responses(cls, obj):
        """get file responses"""
        data = CommunityQuestionResponse.objects.filter(
            question=obj, question__type="File")
        arr = []
        for survey in data:
            arr.append(survey.file)
        return arr

    ratings = serializers.SerializerMethodField()

    @classmethod
    def get_ratings(cls, obj):
        """get ratings of community question response"""
        response1 = CommunityQuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                    question__type="Rating", rating=1).annotate(Count('rating'))
        response2 = CommunityQuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                    question__type="Rating", rating=2).annotate(Count('rating'))
        response3 = CommunityQuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                    question__type="Rating", rating=3).annotate(Count('rating'))
        response4 = CommunityQuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                    question__type="Rating", rating=4).annotate(Count('rating'))
        response5 = CommunityQuestionResponse.objects.values('question__id').filter(question=obj,
                                                                                    question__type="Rating", rating=5).annotate(Count('rating'))
        data = []
        if response1 is not None and len(response1) > 0:
            data.append(response1[0]['rating__count'])
        else:
            data.append(0)
        if response2 is not None and len(response2) > 0:
            data.append(response2[0]['rating__count'])
        else:
            data.append(0)
        if response3 is not None and len(response3) > 0:
            data.append(response3[0]['rating__count'])
        else:
            data.append(0)
        if response4 is not None and len(response4) > 0:
            data.append(response4[0]['rating__count'])
        else:
            data.append(0)
        if response5 is not None and len(response5) > 0:
            data.append(response5[0]['rating__count'])
        else:
            data.append(0)

        return data

    class Meta:
        model = CommunityQuestion
        fields = ['id', 'question', 'choices', 'count',
                  'type',  'text_responses', 'ratings', 'file_responses']


class CommunitySurveyWithResponseSummarySerializer(serializers.ModelSerializer):
    """Community Survey With Response Summary Serializer"""
    count = serializers.SerializerMethodField()

    @classmethod
    def get_count(cls, obj):
        """get count of surveys"""
        data = CommunitySurveyResponse.objects.values(
            'survey__id').filter(survey=obj).annotate(Count('id'))
        if data is not None and len(data) > 0:
            return data[0]['id__count']
        return 0

    questions = serializers.SerializerMethodField()

    @classmethod
    def get_questions(cls, obj):
        """get community question response summary in order"""
        return CommunityQuestionResponseSummarySerializer(CommunityQuestion.objects.filter(survey=obj).order_by('order'),
                                                          many=True).data

    class Meta:
        model = CommunitySurvey
        fields = ['id', 'title', 'link', 'count', 'questions']


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EventTypes


class SmsSurveySerializer(serializers.ModelSerializer):
    eventtype = EventTypeSerializer()

    class Meta:
        fields = '__all__'
        model = SmsSurvey


class SmsSurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SmsSurvey


class SmsSurveyDetailSerializer(serializers.ModelSerializer):
    eventtype = EventTypeSerializer()
    smssend = serializers.SerializerMethodField(read_only=True)
    sms_click_count = serializers.SerializerMethodField(read_only=True)
    sms_submit_count = serializers.SerializerMethodField(read_only=True)
    response_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SmsSurvey
        fields = ('id', 'dispostion', 'citizen_ship',
                  'event_name', 'eventtype', 'from_field', 'smssend', 'sms_click_count', 'sms_submit_count', 'response_rate', 'status',)

    def get_smssend(self, obj):
        data = MessageSendData.objects.filter(
            department=obj.department, event_type__icontains=obj.eventtype.eventtype)
        return data.count()

    def get_sms_click_count(self, obj):
        data = MessageSendData.objects.filter(
            department=obj.department, event_type__icontains=obj.eventtype.eventtype, is_clicked=True)
        return data.count()

    def get_sms_submit_count(self, obj):
        data = MessageSendData.objects.filter(
            department=obj.department, event_type__icontains=obj.eventtype.eventtype, is_submitted=True)
        return data.count()

    def get_response_rate(self, obj):
        return 100


class CreateSmsSurveySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SmsSurvey


class MessageSendDataSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = MessageSendData

    def get_department(self, obj):
        return obj.department.name


class OfficerSurveyDetailSerializer(serializers.ModelSerializer):
    """Officer Serializer"""
    user = UserSerializer(many=False, read_only=True)
    department = DepartmentWithSurveySerializer(many=False, read_only=True)

    class Meta:
        model = Officer
        fields = '__all__'
