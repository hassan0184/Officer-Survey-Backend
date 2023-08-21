import os
from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@officersurvey.com').exists():
            User.objects.create_superuser('admin@officersurvey.com',
                                          '!2!admin!2!')
        if not User.objects.filter(email='admin@departmentinsignt.com').exists():
            User.objects.create_superuser('admin@departmentinsignt.com',
                                          '!2!departmentinsignt!2!')