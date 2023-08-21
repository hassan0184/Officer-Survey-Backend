"""Admin Site ViewSet"""
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from officers_survey.pagination import CustomPagination
from api.serializers import (UserSerializer, DepartmentSerializer,
OfficerSerializer, DistrictSerializer)
from accounts.models import Officer
from department.models import Department, District
from api.utils import sucess_response, not_found_error
from api.views.helper import get_survey_response


class AdminLoginViewSet(APIView):
    """Admin Login ViewSet"""
    def post(self, request):
        """Api For Admin Login"""
        email = request.data.get("email")
        password = request.data.get("password")
        email = email.lower()
        user = authenticate(username=email, password=password)
        if user is not None and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            user = UserSerializer(user)
            content = {
                'success': True,
                'message': '',
                'data': { 'user': user.data, 'is_superuser': True},
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }
            return Response(content)
        return not_found_error('Invalid login credentials')

class DepartmentViewSet(APIView):
    """Department View Set"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch All Departments"""
        departments = Department.objects.all()
        return sucess_response(DepartmentSerializer(departments, many=True).data)


class SurveyResponseByDepartmentViewSet(GenericAPIView):
    """Survey Response By Department ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    def get(self, request, _pk):
        """Fetch Survey Response By Department"""
        try:
            department = Department.objects.get(id=_pk)
            filter_department =  Q(officer__department=department)
            data = get_survey_response(self, request, filter_department)
            if type(data) is Response:
                return data
            return Response(data)
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")


class AdminListOfficersViewSet(APIView):
    """Admin List Officers ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request, _pk):
        """Fetch Officers"""
        department = Department.objects.get(id=_pk)
        search = request.query_params.get("search", "")
        officers = Officer.objects.filter(
            Q(department=department) &
            (
                Q(badge_number__istartswith=search) |
                Q(user__email__istartswith=search) |
                Q(first_name__istartswith=search) |
                Q(last_name__istartswith=search)
            ))
        officers = OfficerSerializer(officers, many=True)
        return sucess_response(officers.data)

class AdminDistrictViewSet(APIView):
    """Admin District ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request, _pk):
        """Fetch Districts"""
        try:
            department = Department.objects.get(id=_pk)
            districts = District.objects.filter(department=department)
            districts = DistrictSerializer(districts, many=True)
            return sucess_response(districts.data)
        except Department.DoesNotExist:
            return not_found_error("Department Not Found")
