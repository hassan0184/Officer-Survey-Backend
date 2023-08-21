"""Department Models"""
import uuid
from django.db import models
from survey.models import Survey, Question, Choice

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

PLANS = (
        ('Community', 'Community'),
        ('Employee', 'Employee'),
        ('Pro', 'Pro'),
        ('Pro and Sms', 'Pro and Sms'),
)


class Department(models.Model):
    """Model to Create Department"""
    name = models.CharField(max_length=40, unique=True)
    header = models.ImageField(default='departmentHeader/default_background.png',
                               upload_to='departmentHeader')
    phone = models.CharField(max_length=40, blank=True)
    telephone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True, choices=STATES)
    zip_code = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=10, editable=False, unique=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    no_of_days = models.IntegerField(default=30)
    plan = models.CharField(max_length=200, blank=True,
                            choices=PLANS, default='Basic')
    trigger_rating = models.IntegerField(default=2)
    is_suspend = models.BooleanField(default=False)
    records_readed = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """method that save department model with the logic below"""
        self.name = self.name.replace(" ", "")
        self.link = uuid.uuid4().hex[:9].upper()
        survey = Survey.objects.get(name="Sample Survey")
        if self.survey.id == survey.id:
            old_survey = self.survey
            new_survey = Survey.objects.get(pk=self.survey.id)
            new_survey.pk = None
            new_survey.name = "Survey - " + self.name
            new_survey.save()
            self.survey = new_survey
            questions = Question.objects.filter(
                survey=old_survey).order_by('id')
            new_questions = []
            for question in questions.iterator():
                new_question = Question.objects.get(pk=question.id)
                new_question.pk = None
                new_question.survey = new_survey
                new_questions.append(new_question)
            Question.objects.bulk_create(new_questions)
            for i in range(len(new_questions)):
                new_choices = []
                choices = Choice.objects.filter(question=questions[i])
                for choice in choices.iterator():
                    new_choice = Choice.objects.get(pk=choice.id)
                    new_choice.pk = None
                    new_choice.question = new_questions[i]
                    new_choices.append(new_choice)
                Choice.objects.bulk_create(new_choices)
        super().save(*args, **kwargs)

    def __str__(self):
        """retrun name of department"""
        return self.name


class District(models.Model):
    """Model to Create District of Different Department"""
    name = models.CharField(max_length=40)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        """return name of district"""
        return self.name


class Support(models.Model):
    """Model to Create Support for User"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pic = models.FileField(upload_to='support', null=True, blank=True)
    user = models.ForeignKey('accounts.Officer', on_delete=models.CASCADE)

    def __str__(self):
        """return title of suuport"""
        return self.title
