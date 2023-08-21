import os
from django.core.management.base import BaseCommand
from accounts.models import User
from department.models import Department
from survey.models import Survey, SurveyResponse, QuestionResponse
from accounts.models import *
import datetime
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        if Department.objects.filter(name='TestDepartment').exists():
            department = Department.objects.get(name='TestDepartment')
            officers = Officer.objects.filter(department=department)
            for officer in officers:
                user = User.objects.get(pk=officer.user.id)
                survey_responses = SurveyResponse.objects.filter(officer=officer)
                for survey_response in survey_responses:
                    question_responses = QuestionResponse.objects.filter(survey=survey_response)
                    for question_response in question_responses:
                        question_response.delete()
                    survey_response.delete()
                user.delete()
                officers.delete()
            surveys = Survey.objects.filter(pk=department.survey.id)
            for survey in surveys:
                survey.delete()
                pass
            department.delete()
            pass

