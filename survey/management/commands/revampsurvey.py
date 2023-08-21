import os
from django.core.management.base import BaseCommand
from accounts.models import User, Group
from survey.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        surveies = Survey.objects.all()
        for survey in surveies:
            questions = Question.objects.filter(survey=survey)
            for question in questions:
                question.save()
                choices = Choice.objects.filter(question=question)
                for choice in choices:
                    choice.save()