"""Response and Some Helper Methods"""
import random
import string
import os
import datetime
import requests
from decouple import config
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Q
from django.http import HttpResponse
from xlrd import open_workbook
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from survey.models import (SurveyResponse, QuestionResponse, Employee360SurveyResponse,
                           Employee360QuestionResponse, CommunitySurveyResponse, CommunityQuestionResponse)
from accounts.models import User, Officer
import pandas as pd


date_format = "%m-%d-%Y"
date_time_format = date_format + " %H:%M %p"


def bad_request_error(message):
    """bad request error response"""
    content = {
        'success': False,
        'message': message
    }
    return Response(content, status.HTTP_400_BAD_REQUEST)


def maximum_length_error(message):
    '''maximum length error'''
    content = {
        'success': False,
        'message': message
    }
    return Response(content, status.HTTP_400_BAD_REQUEST)


def not_found_error(message):
    """not found error response"""
    content = {
        'success': False,
        'message': message
    }
    return Response(content, status.HTTP_404_NOT_FOUND)


def already_exist_error(message):
    """already exist error response"""
    content = {
        'success': False,
        'message': message
    }
    return Response(content, status.HTTP_409_CONFLICT)


def sucess_response(data, message=''):
    """sucess response response"""
    content = {
        'success': True,
        'message': message,
        'data': data
    }
    return Response(content)


def send_review_email(subject, message, email_to):
    """send review email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        [email_to],
        fail_silently=False
    )


def send_reset_password_email(email_to, code):
    """send reset password email response"""
    send_mail(
        "Please verify your email address",
        "Your verification code is " + code,
        'Officer Survey',
        [email_to],
        fail_silently=False
    )


def send_account_created_email(subject, message, email_to):
    """send account created email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        [email_to],
        fail_silently=False
    )


def send_request_change_email(subject, message, email_to):
    """send request change email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        [email_to],
        fail_silently=False
    )


def send_request_approved_email(subject, message, email_to):
    """send request approved email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        [email_to],
        fail_silently=False
    )


def send_issue_email(subject, message):
    """send issue email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        ['support@officersurvey.com'],
        fail_silently=False
    )


def send_demo_email(subject, message):
    """send demo email response"""
    send_mail(
        subject,
        message,
        'Officer Survey',
        ['support@officersurvey.com'],
        fail_silently=False
    )


def export_data_to_pdf(officer, start_date, end_date, hours):
    """export data to pdf"""
    file_name = officer.badge_number+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    if start_date is not None:
        survey_responses = SurveyResponse.objects.filter(Q(officer=officer) & Q(
            created_at__gte=start_date) & Q(created_at__lte=end_date)).order_by('created_at')
    else:
        survey_responses = SurveyResponse.objects.filter(
            Q(officer=officer)).order_by('created_at')
    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    for survey_response in survey_responses:
        paragraph = Paragraph("Citizen : " + survey_response.first_name +
                              " " + survey_response.last_name, styles['Heading1'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Address : " +
                              survey_response.get_address(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Phone : " +
                              survey_response.get_phone(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Survey at : " + survey_response.get_survey_date(hours), styles["Heading4"])
        story.append(paragraph)

        question_responses = QuestionResponse.objects.filter(
            survey=survey_response.id)

        for question_response in question_responses:
            paragraph = Paragraph(
                "Question : " + question_response.question.question, styles['Normal'])
            story.append(paragraph)
            paragraph = Paragraph(
                "Answer : " + question_response.get_answer(), styles['Normal'])
            story.append(paragraph)

        story.append(PageBreak())

    doc.build(story)

    file_system = FileSystemStorage("/tmp")
    with file_system.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response


def export_department_data_to_pdf(department):
    """export department data to pdf"""
    file_name = department.name+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    survey_responses = SurveyResponse.objects.filter(
        Q(officer__department=department)).order_by('created_at')
    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    for survey_response in survey_responses:
        paragraph = Paragraph("Officer Name : " + survey_response.officer.first_name +
                              " " + survey_response.officer.last_name, styles['Heading1'])
        story.append(paragraph)
        paragraph = Paragraph("Officer Badge Number : " +
                              survey_response.officer.badge_number, styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Officer Email : " + survey_response.officer.user.email, styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen : " + survey_response.first_name +
                              " " + survey_response.last_name, styles['Heading1'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Address : " +
                              survey_response.get_address(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Phone : " +
                              survey_response.get_phone(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Survey at : " + survey_response.get_survey_date(), styles["Heading4"])
        story.append(paragraph)

        question_responses = QuestionResponse.objects.filter(
            survey=survey_response.id)

        for question_response in question_responses:
            paragraph = Paragraph(
                "Question : " + question_response.question.question, styles['Normal'])
            story.append(paragraph)
            paragraph = Paragraph(
                "Answer : " + question_response.get_answer(), styles['Normal'])
            story.append(paragraph)

        story.append(PageBreak())

    doc.build(story)

    file_system = FileSystemStorage("/tmp")
    with file_system.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response


PASSWORD = "password"
officer_file = 'officers.xlsx'


def handle_uploaded_file(request, file):
    """handle uploaded file"""
    base_link = None
    if os.environ.get('BASE_URL') is None:
        base_link = config('BASE_URL')
    else:
        base_link = os.environ['BASE_URL']
    if file.content_type == 'text/csv':
        reader = pd.read_csv(file)
        reader.to_excel(officer_file, index=None, header=True)
        work_book = open_workbook(officer_file)
    else:
        work_book = open_workbook(file_contents=file.read())
    values = []
    for sheet in work_book.sheets():
        for row in range(1, sheet.nrows):
            col_names = sheet.row(0)
            col_value = []
            for name, col in zip(col_names, range(sheet.ncols)):
                value = (sheet.cell(row, col).value)
                col_value.append((name.value, value))
            values.append(col_value)
    print(values)
    officers = []
    officers_user = []
    message = ""
    for index, row in enumerate(values):
        line_no = index + 2
        if validate_tuple(row) is True:
            if user_email_not_exist(get_value_from_tuple(row, 'email')):
                if user_email_not_exist_in_this_list(officers_user, get_value_from_tuple(row, 'email')):
                    user = User(
                        email=get_value_from_tuple(row, 'email'))
                    user.set_password(PASSWORD)
                    officers_user.append(user)
                    supervisor = Officer.objects.get(
                        user=request.user, is_supervisor=True)
                    department = supervisor.department
                    officer = Officer(
                        user=user,
                        first_name=get_value_from_tuple(row, 'first name'),
                        last_name=get_value_from_tuple(row, 'last name'),
                        badge_number=get_value_from_tuple(row, 'badge number'),
                        address=get_value_from_tuple(row, 'address'),
                        city=get_value_from_tuple(row, 'city'),
                        state=get_value_from_tuple(row, 'state'),
                        zip_code=get_value_from_tuple(row, 'zip code'),
                        department=department)
                    officers.append(officer)
                else:
                    message = "There is an issue in row "+str(line_no) + ". The email " + get_value_from_tuple(row, 'email') + " is already in this list at row " + str(
                        user_email_exist_row_number(officers_user, get_value_from_tuple(row, 'email'))) + ". Kindly update it and reupload all data."
                    break
            else:
                message = "There is an issue in row "+str(line_no) + ". The email " + get_value_from_tuple(
                    row, 'email') + " is already registered. Kindly update it and reupload all data."
                break
        else:
            message = "There is an format issue in row " + \
                str(line_no) + ". Either there is some required field missing or email is not valid. Follow the sample sheet. Kindly update it and reupload all data."
            break
        print(row)
    if message != "":
        print(message)
    else:
        for i in range(len(officers_user)):
            user = officers_user[i]
            user.save()
            officers[i].save()
            send_account_created_email("Account Created", "Your Officer Survey account has been created. To complete your registration process you must login and change your password. \n\nEmail : " + user.email + "\nPassword : " + PASSWORD + "\n\nClick here to login " +
                                       base_link + "/login \n\nIf you have questions or need help, please contact the appropriate personnel in your department. \n\nThis message was sent from an automated system that cannot receive emails. Please do not reply to this message", user.email)
    return message


def get_value_from_tuple(row, name):
    """get value from tuple"""
    for item in row:
        if item[0].lower() == name:
            return str(item[1])
    return ''


def validate_tuple(row):
    """method that validate tuple"""
    valid = []
    for item in row:
        if item[0].lower() == "first name":
            valid.append(item[1] != "")
        elif item[0].lower() == "last name":
            valid.append(item[1] != "")
        elif item[0].lower() == "badge number":
            valid.append(item[1] != "")
        elif item[0].lower() == "email":
            if item[1] != "":
                try:
                    validate_email(item[1])
                except ValidationError:
                    valid.append(False)
                else:
                    valid.append(True)
            else:
                valid.append(False)
    if len(valid) < 4:
        return False
    for _v in valid:
        if _v is False:
            return False
    return True


def user_email_not_exist(email):
    """user email not exist"""
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return True
    return False


def user_email_not_exist_in_this_list(arr, email):
    """user email not exist in this list"""
    for user in arr:
        if user.email == email:
            return False
    return True


def user_email_exist_row_number(arr, email):
    """user email exist row number"""
    for index, user in enumerate(arr):
        if user.email == email:
            return index + 2
    return -1


def export_notes_data_to_pdf(notes, officer, hours):
    """export notes data to pdf"""
    file_name = officer.badge_number+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    paragraph = Paragraph(officer.get_name(), styles['Heading1'])
    story.append(paragraph)
    for note in notes:
        paragraph = Paragraph("Notes : " + note.notes, styles['Heading3'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Created at: " + note.get_notes_date(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Posted by : " + note.notes_by.get_name(), styles['Heading4'])
        story.append(paragraph)
        story.append(PageBreak())

    doc.build(story)

    file_system = FileSystemStorage("/tmp")
    with file_system.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response


def get_lat_long(zip_code):
    """get lat long"""
    location = {}
    url_location = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=geometry,formatted_address&key=AIzaSyDcpGAfaBR1uFQvki-3z46SOB883GSoTcU"
    location_response = requests.get(url_location.format(zip_code)).json()
    if len(location_response['candidates']) > 0:
        location['lat'] = location_response['candidates'][0]['geometry']['location']['lat']
        location['lng'] = location_response['candidates'][0]['geometry']['location']['lng']
        location['place'] = location_response['candidates'][0]['formatted_address']

    return location


def export_employee_360_data_to_pdf(survey, hours):
    """export employee360 data to pdf"""
    file_name = survey.title+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    survey_responses = Employee360SurveyResponse.objects.filter(
        survey=survey).order_by('created_at')
    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    paragraph = Paragraph(survey.title, styles["Heading2"])
    story.append(paragraph)
    paragraph = Paragraph("Number of Responses: " +
                          str(len(survey_responses)), styles["Heading4"])
    story.append(paragraph)
    for survey_response in survey_responses:
        paragraph = Paragraph(
            "Survey at : " + survey_response.get_survey_date(hours), styles["Heading4"])
        story.append(paragraph)

        question_responses = Employee360QuestionResponse.objects.filter(
            survey=survey_response.id)

        for question_response in question_responses:
            paragraph = Paragraph(
                "Question : " + question_response.question.question, styles['Normal'])
            story.append(paragraph)
            paragraph = Paragraph(
                "Answer : " + question_response.get_answer(), styles['Normal'])
            story.append(paragraph)

        paragraph = Paragraph("  ", styles['Normal'])
        story.append(paragraph)
        story.append(paragraph)
        story.append(paragraph)

    doc.build(story)

    file_system = FileSystemStorage("/tmp")
    with file_system.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response


def export_community_data_to_pdf(survey, hours):
    """export community data to pdf"""
    file_name = survey.title+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    survey_responses = CommunitySurveyResponse.objects.filter(
        survey=survey).order_by('created_at')
    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    paragraph = Paragraph(survey.title, styles["Heading2"])
    story.append(paragraph)
    paragraph = Paragraph("Number of Responses: " +
                          str(len(survey_responses)), styles["Heading4"])
    story.append(paragraph)
    for survey_response in survey_responses:
        paragraph = Paragraph(
            "Survey at : " + survey_response.get_survey_date(hours), styles["Heading4"])
        story.append(paragraph)

        question_responses = CommunityQuestionResponse.objects.filter(
            survey=survey_response.id)

        for question_response in question_responses:
            paragraph = Paragraph(
                "Question : " + question_response.question.question, styles['Normal'])
            story.append(paragraph)
            paragraph = Paragraph(
                "Answer : " + question_response.get_answer(), styles['Normal'])
            story.append(paragraph)

        paragraph = Paragraph("  ", styles['Normal'])
        story.append(paragraph)
        story.append(paragraph)
        story.append(paragraph)

    doc.build(story)

    file_system = FileSystemStorage("/tmp")
    with file_system.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response


def export_demographic_data_to_pdf(department, start_date, end_date, hours, officer=None):
    """export demographic data to pdf"""
    if department is not None:
        file_name = department.name+".pdf"
    elif officer is not None:
        file_name = officer.badge_number+".pdf"
    doc = SimpleDocTemplate("/tmp/" + file_name)
    if start_date is not None:
        if officer is None:
            survey_responses = SurveyResponse.objects.filter(Q(officer__department=department) & Q(
                created_at__gte=start_date) & Q(created_at__lte=end_date)).order_by('created_at')
        else:
            survey_responses = SurveyResponse.objects.filter(Q(officer=officer) & Q(
                created_at__gte=start_date) & Q(created_at__lte=end_date)).order_by('created_at')

    else:
        if officer is None:
            survey_responses = SurveyResponse.objects.filter(
                Q(officer__department=department)).order_by('created_at')
        else:
            survey_responses = SurveyResponse.objects.filter(
                Q(officer=officer)).order_by('created_at')

    styles = getSampleStyleSheet()
    story = [Spacer(0, 0)]
    for survey_response in survey_responses:
        paragraph = Paragraph("Officer Name : " + survey_response.officer.first_name +
                              " " + survey_response.officer.last_name, styles['Heading1'])
        story.append(paragraph)
        paragraph = Paragraph("Officer Badge Number : " +
                              survey_response.officer.badge_number, styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Officer Email : " + survey_response.officer.user.email, styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen : " + survey_response.first_name +
                              " " + survey_response.last_name, styles['Heading1'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Address : " +
                              survey_response.get_address(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph("Citizen Phone : " +
                              survey_response.get_phone(), styles['Heading4'])
        story.append(paragraph)
        paragraph = Paragraph(
            "Survey at : " + survey_response.get_survey_date(hours), styles["Heading4"])
        story.append(paragraph)

        question_responses = QuestionResponse.objects.filter(
            survey=survey_response.id)

        for question_response in question_responses:
            _p = Paragraph(
                "Question : " + question_response.question.question, styles['Normal'])
            story.append(_p)
            _p = Paragraph(
                "Answer : " + question_response.get_answer(), styles['Normal'])
            story.append(_p)

        story.append(PageBreak())
    doc.build(story)

    _fs = FileSystemStorage("/tmp")
    with _fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
        return response

    return response


def end_date_update(request, end_date):
    """method to update end date"""
    date_now = request.query_params.get("date_now")
    if date_now:
        date_now = datetime.datetime.strptime(date_now, date_time_format)
        if end_date.day == date_now.day - 1:
            end_date = end_date + datetime.timedelta(hours=12)
    return end_date


def create_new_ref_number():
    return ''.join([random.choice(string.ascii_letters
                                  + string.digits) for n in range(5)])
