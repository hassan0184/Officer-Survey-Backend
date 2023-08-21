from django.core.management.base import BaseCommand, CommandError
from events.models import SmsSurvey, MessageSendData
from department.models import Department
from decouple import config
import os
from twilio.rest import Client
import psycopg2
from psycopg2 import Error
from department.models import Department
from events.models import DatabaseDepartments
import threading


def database_connect(departmentid, user, password, host, port, database):
    """post request api to send messages"""
    if 'TWILIO_ACCOUNT_SID' in os.environ:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIIO_AUTH_TOKEN']
        front_end_url = os.environ['FRONTEND_URL']
    else:
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIIO_AUTH_TOKEN')
        front_end_url = config('FRONTEND_URL')

    whatsapp_num = '4436489738'
    client = Client(account_sid, auth_token)
    department = Department.objects.get(id=departmentid)
    department_name = department.name
    is_sms = SmsSurvey.objects.filter(department=department).first()
    if is_sms is None:
        return

    read_check = department.records_readed
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        postgreSQL_select_Query = """SELECT * FROM public."Records"  WHERE  id > {read_check};""".format(
            read_check=read_check)

        cursor.execute(postgreSQL_select_Query)
        new_records = cursor.fetchall()
        for record in new_records:
            sms_survey = SmsSurvey.objects.filter(
                department=department, eventtype__eventtype__icontains=record[3], status=True).first()
            if sms_survey != None:
                message_data_obj = MessageSendData(
                    user_name=record[1], department=department, event_type=record[3])
                message_data_obj.save()

                message = sms_survey.from_field + '  '+str(front_end_url) + \
                    'department/' + department_name + '?ref='+message_data_obj.refrence
                message = client.messages.create(
                    from_=whatsapp_num,
                    body=message,
                    to=str(record[0])
                )
        department.records_readed = read_check+len(new_records)
        department.save()

    except (Exception, Error) as error:
        return
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return


class Command(BaseCommand):
    def handle(self, *args, **options):

        database_instances = DatabaseDepartments.objects.filter(status=True)
        thread_list = []

        for instance in database_instances:
            user = instance.user
            password = instance.password
            host = instance.host
            port = instance.port
            database = instance.database
            department_id = instance.department.id

            t = threading.Thread(target=database_connect, args=(
                department_id, user, password, host, port, database))
            thread_list.append(t)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        return
