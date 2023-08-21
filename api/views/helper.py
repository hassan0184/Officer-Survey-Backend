from accounts.models import *
from department.models import *
from api.utils import *
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Avg
from api.serializers import SurveyResponseForGraphSerializer, SurveyResponseSerializer
import datetime
from django.db.models import Q
from api.utils import end_date_update, date_format
from survey.models import SurveyResponse


def add_officer(request, department):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")
    badge_number = request.data.get("badge_number")
    district = request.data.get("district")
    phone = request.data.get("phone", "")
    address = request.data.get("address", "")
    city = request.data.get("city", "")
    zip_code = request.data.get("zip_code", "")
    state = request.data.get("state", "")
    link = uuid.uuid4().hex[:9].upper()
    is_supervisor = request.data.get("is_supervisor", False)
    if is_supervisor == 'true':
        is_supervisor = True
    else:
        is_supervisor = False
    profile_pic = request.data.get("profile_pic")
    if district is not None:
        try:
            district = District.objects.get(id=district)
        except:
            return not_found_error('District Not Found')
    if email is None:
        return not_found_error('Email Not Found')
    if password is None:
        return not_found_error('Password Not Found')
    if first_name is None:
        return not_found_error('First Name Not Found')
    if last_name is None:
        return not_found_error('Last Name Not Found')
    if badge_number is None:
        return not_found_error('Badge Number Not Found')
    try:
        if profile_pic is None:
            profile_pic = 'default_profie_pic.png'
        user = User(email=email.lower(), profile_pic=profile_pic)
        user.password = make_password(password)
        user.save()
    except:
        return already_exist_error('Email already exist')
    officer = Officer(
        user=user,
        first_name=first_name,
        last_name=last_name,
        badge_number=badge_number,
        department=department,
        district=district,
        phone=phone,
        address=address,
        city=city,
        zip_code=zip_code,
        state=state,
        is_supervisor=is_supervisor,
        link=link
    )
    officer.save()
    return officer


def update_officer(request, officer):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")
    badge_number = request.data.get("badge_number")
    district = request.data.get("district")
    phone = request.data.get("phone", "")
    address = request.data.get("address", "")
    city = request.data.get("city", "")
    zip_code = request.data.get("zip_code", "")
    state = request.data.get("state", "")
    is_supervisor = request.data.get("is_supervisor", False)
    if is_supervisor == 'true':
        is_supervisor = True
    else:
        is_supervisor = False
    profile_pic = request.data.get("profile_pic")
    is_profile_pic_change = request.data.get("is_profile_pic_change", 'false')
    if district is not None:
        try:
            district = District.objects.get(id=district)
        except:
            return not_found_error('District Not Found')
    if email is None:
        return not_found_error('Email Not Found')
    if is_profile_pic_change is None:
        return not_found_error('Tell if profile pic need to chnage')
    if first_name is None:
        return not_found_error('First Name Not Found')
    if last_name is None:
        return not_found_error('Last Name Not Found')
    if badge_number is None:
        return not_found_error('Badge Number Not Found')
    try:
        officer.user.email = email.lower()
        if is_profile_pic_change == 'true':
            officer.user.profile_pic = profile_pic
        officer.user.save()
    except:
        return already_exist_error('Email already exist')

    officer.first_name = first_name
    officer.last_name = last_name
    officer.badge_number = badge_number
    officer.district = district
    officer.phone = phone
    officer.address = address
    officer.city = city
    officer.zip_code = zip_code
    officer.state = state
    officer.is_supervisor = is_supervisor
    officer.save()
    return officer


def get_survey_response(self, request, filter=None):
    rating = request.query_params.get("rating")
    district = request.query_params.get("district")
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    citizen_name = request.query_params.get("citizen_name")
    if rating is not None:
        filter = filter & Q(rating=rating)
    if district is not None:
        try:
            district = District.objects.get(id=district)
            filter = filter & Q(officer__district=district)
        except:
            return not_found_error('District Not Found')
    if start_date is not None:
        start_date = datetime.datetime.strptime(start_date, date_format)
        filter = filter & Q(created_at__gte=start_date)
    if end_date is not None:
        end_date = datetime.datetime.strptime(end_date, date_format)
        end_date = end_date_update(request, end_date)
        end_date = end_date + datetime.timedelta(days=1)
        filter = filter & Q(created_at__lte=end_date)
    if citizen_name is not None:
        first_name = last_name = citizen_name
        if (citizen_name != ''):
            citizen_name = citizen_name.split()
            first_name = citizen_name[0]
        if type(citizen_name) is list and len(citizen_name) > 1:
            last_name = citizen_name[1]
            filter = filter & (Q(first_name__istartswith=first_name) & Q(last_name__istartswith=last_name))
        else:
            filter = filter & (Q(first_name__istartswith=first_name) | Q(last_name__istartswith=last_name))
    survey_responses = SurveyResponse.objects.filter(filter).order_by('-created_at')
    pie_chat = [
        SurveyResponse.objects.filter(Q(filter) & Q(rating=1)).aggregate(Count('rating'))['rating__count'],
        SurveyResponse.objects.filter(Q(filter) & Q(rating=2)).aggregate(Count('rating'))['rating__count'],
        SurveyResponse.objects.filter(Q(filter) & Q(rating=3)).aggregate(Count('rating'))['rating__count'],
        SurveyResponse.objects.filter(Q(filter) & Q(rating=4)).aggregate(Count('rating'))['rating__count'],
        SurveyResponse.objects.filter(Q(filter) & Q(rating=5)).aggregate(Count('rating'))['rating__count']
    ]
    avg_rating = SurveyResponse.objects.filter(Q(filter)).aggregate(Avg('rating'))['rating__avg']
    query = SurveyResponse.objects.values('created_at__date').filter(
        Q(filter)).annotate(Avg('rating')).order_by('created_at__date')
    graph_serializer = SurveyResponseForGraphSerializer(query, many=True)
    page = self.paginate_queryset(survey_responses)
    if page is not None:
        serializer = SurveyResponseSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
    else:
        serializer = SurveyResponseSerializer(survey_responses, many=True)
        data = serializer.data
    if avg_rating is None:
        avg_rating = 0
    data['pie_chart'] = pie_chat
    data['avg_rating'] = round(avg_rating, 2)
    data['line_graph'] = graph_serializer.data
    return data
