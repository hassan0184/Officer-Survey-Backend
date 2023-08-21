from django.core.management.base import BaseCommand
from sqlalchemy import null
from survey.models import CommunitySurvey, Employee360Survey


class Command(BaseCommand):
    def handle(self, *args, **options):
        Surveys = CommunitySurvey.objects.filter(
            survery_category="Everything Else Surveys").update(survery_category='Everything')

        emp_Surveys = Employee360Survey.objects.filter(
            survery_category="Everything Else Surveys").update(survery_category='Everything')
