"""Models related to Survey"""
from operator import mod
from os import environ
from pyexpat import model
from statistics import mode
from django.db import models
from django.utils import timezone
from google.cloud import translate
from decouple import config
from datetime import timedelta

from grpc import Status
from sqlalchemy import true
from api.choice_fields import Category_Employee, Category_Survey

STATES = (
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('D.C', 'D.C'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('Indiana', 'Indiana'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
)

QUESTION_CHOICES = (
    ("Multiple Choice", "Multiple Choice"),
    ("Drop Down", "Drop Down"),
    ("Text Area", "Text Area"),
    ("Rating", "Rating"),
    ("Poll", "Poll"),
    ("Vote", "Vote"),
    ("Checkbox", "Checkbox"),
    ("File", "File"),
)

LANGUAGE_CHOICES = (
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("ar", "Arabic"),
    ("ko", "Korean"),
    ('zh-CN', 'Chinese (Simplified)')
)

CALL_BACK_STATE = (
    ("Requested", "Requested"),
    ("Reviewed", "Reviewed")
)

SURVEY_TYPE = (
    ("Survey", "Survey"),
    ("Poll", "Poll")
)


def translate_text(text, language='de'):
    """method to translate text"""
    project_id = environ.get("GOOGLE_TRANSLATE_PROJECT_ID", "")
    if project_id == "":
        project_id = config('GOOGLE_TRANSLATE_PROJECT_ID')
    assert project_id
    parent = f"projects/{project_id}"
    client = translate.TranslationServiceClient()
    result = client.translate_text(
        contents=[text], target_language_code=language, parent=parent)
    for translation in result.translations:
        return translation.translated_text
    return "Not Avaiable"

# Create your models here.


class Survey(models.Model):
    """Survey Model"""
    name = models.CharField(default="Sample Survey",
                            max_length=100, unique=True)
    about = models.TextField(max_length=300)

    def __str__(self):
        """return survey name"""
        return self.name


class Question(models.Model):
    """Question Model"""
    question = models.CharField(max_length=200)
    type = models.CharField(choices=QUESTION_CHOICES,
                            max_length=100, default="Mutiple Choice")
    survey = models.ForeignKey(
        Survey, related_name="questions", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    required = models.BooleanField(default=True)

    def __str__(self):
        """return qustion and survey name"""
        return self.question + " - " + self.survey.name


class QuestionTranslation(models.Model):
    """Question Translation Model"""
    text = models.CharField(max_length=200)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=100, default="English")
    question = models.ForeignKey(Question, related_name="question_translation",
                                 on_delete=models.CASCADE)

    def __str__(self):
        """return text and question"""
        return self.text + " - " + self.question.question


class Choice(models.Model):
    """Choice Model"""
    choice = models.CharField(max_length=100)
    show_comment_box = models.BooleanField(default=False)
    comment_box_place_holder = models.CharField(max_length=100, blank=True)
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE)

    def __str__(self):
        """return choice, question and its survey name"""
        return self.choice + " - " + self.question.question + " - " + self.question.survey.name


class ChoiceTranslation(models.Model):
    """Choice Translation"""
    text = models.CharField(max_length=200)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=100, default="English")
    choice = models.ForeignKey(
        Choice, related_name="choice_translation", on_delete=models.CASCADE)

    def __str__(self):
        """return text"""
        return self.text


class SurveyResponse(models.Model):
    """Survey Response Model"""
    officer = models.ForeignKey("accounts.Officer",  on_delete=models.CASCADE,
                                related_name='surveyed_officer')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.CharField(max_length=800, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True, choices=STATES)
    zip_code = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    request_change = models.BooleanField(default=False)
    comment_reason = models.CharField(max_length=800, blank=True)
    changed_by_supervisor = models.BooleanField(default=False)
    change_reason = models.CharField(max_length=200, blank=True)
    reviewed_by_supervisor = models.ForeignKey("accounts.Officer", null=True,
                                               on_delete=models.SET_NULL, related_name='reviewed_by_supervisor')

    def __str__(self):
        """return first_name"""
        return self.first_name

    def get_address(self):
        """return address,city,state and zip_code"""
        return self.address + " " + self.city + " " + self.state + " " + self.zip_code

    def get_name(self):
        """return first_name and last_name"""
        return self.first_name + " " + self.last_name

    def get_phone(self):
        """return phone"""
        return self.phone

    def get_survey_date(self, hours=None):
        """return date"""
        created_at = self.created_at
        if hours is not None:
            created_at = created_at + timedelta(minutes=int(hours))
        return created_at.strftime("%Y-%m-%d, %H:%M:%S")


class QuestionResponse(models.Model):
    """Question Response"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(SurveyResponse, related_name="questions_response",
                               on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    comment_box = models.CharField(max_length=800, blank=True)

    def __str__(self):
        """return question"""
        return self.question.question

    def get_answer(self):
        """return either comment_box or choice"""
        if self.question.type == 'Text Area':
            return self.comment_box
        return self.choice.choice


class CallBack(models.Model):
    """CallBack Model"""
    survey = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=CALL_BACK_STATE,
                              max_length=100, default="Requested")


class CallBackNotes(models.Model):
    """CallBackNotes Model"""
    reviewed_by_supervisor = models.ForeignKey("accounts.Officer", null=True,
                                               on_delete=models.SET_NULL, related_name='call_back_reviewed_by_supervisor')
    notes_by_supervivor = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    callback = models.ForeignKey(
        CallBack, on_delete=models.CASCADE, related_name="notes")


class Employee360Survey(models.Model):
    """Employee360Survey Model"""
    title = models.CharField(
        default="Sample 360 Employee Survey", max_length=100)
    instruction = models.TextField(max_length=500)
    type = models.CharField(choices=SURVEY_TYPE,
                            max_length=100, default="Survey")
    link = models.CharField(max_length=10, editable=False, unique=True)
    department = models.ForeignKey(
        "department.Department", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expire = models.DateTimeField(null=True)
    survery_category = models.CharField(
        choices=Category_Employee.choices, default=Category_Employee.Everything_Else, max_length=50)

    def __str__(self):
        """return title"""
        return self.title


class Employee360Question(models.Model):
    """Employee360Question Model"""
    question = models.CharField(max_length=200)
    type = models.CharField(choices=QUESTION_CHOICES,
                            max_length=100, default="Mutiple Choice")
    survey = models.ForeignKey(Employee360Survey, related_name="questions",
                               on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    required = models.BooleanField(default=True)

    def __str__(self):
        """return question and survey title"""
        return self.question + " - " + self.survey.title


class Employee360Choice(models.Model):
    """Employee360Choice Model"""
    choice = models.CharField(max_length=100)
    question = models.ForeignKey(Employee360Question, related_name="choices",
                                 on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        """return choice, question and survey title"""
        return self.choice + " - " + self.question.question + " - " + self.question.survey.title


class Employee360SurveyResponse(models.Model):
    """Employee360SurveyResponse Model"""
    survey = models.ForeignKey(Employee360Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_survey_date(self, hours=None):
        """return date of survey"""
        created_at = self.created_at
        if hours is not None:
            created_at = created_at + timedelta(minutes=int(hours))
        return created_at.strftime("%Y-%m-%d, %H:%M:%S")


class Employee360QuestionResponse(models.Model):
    """Employee360QuestionResponse Model"""
    question = models.ForeignKey(Employee360Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Employee360SurveyResponse, related_name="questions_response",
                               on_delete=models.CASCADE)
    choice = models.ForeignKey(
        Employee360Choice, on_delete=models.CASCADE, null=True)
    comment_box = models.CharField(max_length=800, blank=True)
    rating = models.IntegerField(null=True)
    file = models.FileField(upload_to='employee360Files', null=True)

    def __str__(self):
        """return question"""
        return self.question.question

    def get_answer(self):
        """return answer related to type of question"""
        if self.question.type == 'Text Area':
            return self.comment_box
        if self.question.type == 'Rating':
            return str(self.rating)
        return self.choice.choice


class CommunitySurvey(models.Model):
    """CommunitySurvey Model """

    title = models.CharField(
        default="Community Employee Survey", max_length=100)
    instruction = models.TextField(max_length=500)
    type = models.CharField(choices=SURVEY_TYPE,
                            max_length=100, default="Survey")
    link = models.CharField(max_length=10, editable=False, unique=True)
    department = models.ForeignKey(
        "department.Department", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expire = models.DateTimeField(null=True)
    survery_category = models.CharField(
        choices=Category_Survey.choices, default=Category_Survey.Everything_Else, max_length=50)

    def __str__(self):
        """return title"""
        return self.title


class CommunityQuestion(models.Model):
    """CommunityQuestion Model"""
    question = models.CharField(max_length=200)
    type = models.CharField(choices=QUESTION_CHOICES,
                            max_length=100, default="Mutiple Choice")
    survey = models.ForeignKey(CommunitySurvey, related_name="questions",
                               on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    required = models.BooleanField(default=True)

    def __str__(self):
        """return question and survey title"""
        return self.question + " - " + self.survey.title


class CommunityChoice(models.Model):
    """CommunityChoice Model"""
    choice = models.CharField(max_length=100)
    question = models.ForeignKey(CommunityQuestion, related_name="choices",
                                 on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        """return choice, question and survey's title"""
        return self.choice + " - " + self.question.question + " - " + self.question.survey.title


class CommunitySurveyResponse(models.Model):
    """CommunitySurveyResponse Model"""
    survey = models.ForeignKey(CommunitySurvey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_survey_date(self, hours=None):
        """return date of survey"""
        created_at = self.created_at
        if hours is not None:
            created_at = created_at + timedelta(minutes=int(hours))
        return created_at.strftime("%Y-%m-%d, %H:%M:%S")


class CommunityQuestionResponse(models.Model):
    """CommunityQuestionResponse Model"""
    question = models.ForeignKey(CommunityQuestion, on_delete=models.CASCADE)
    survey = models.ForeignKey(CommunitySurveyResponse, related_name="questions_response",
                               on_delete=models.CASCADE)
    choice = models.ForeignKey(
        CommunityChoice, on_delete=models.CASCADE, null=True)
    comment_box = models.CharField(max_length=800, blank=True)
    rating = models.IntegerField(null=True)
    file = models.FileField(upload_to='communityFiles', null=True)

    def __str__(self):
        """return question"""
        return self.question.question

    def get_answer(self):
        """return answer related to type of question"""
        if self.question.type == 'Text Area':
            return self.comment_box
        if self.question.type == 'Rating':
            return str(self.rating)
        return self.choice.choice
