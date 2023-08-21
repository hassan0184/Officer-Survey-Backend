import os
from django.core.management.base import BaseCommand
from sqlalchemy import null
from accounts.models import Officer
import uuid


class Command(BaseCommand):
    def handle(self, *args, **options):
        officers = Officer.objects.filter(link=None)

        for officer in officers:
            officer.link = uuid.uuid4().hex[:9].upper()
            officer.save()
