"""District Related ViewSet"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import DistrictSerializer
from accounts.models import Officer
from api.utils import sucess_response, not_found_error
from department.models import District


class DistrictViewSet(APIView):
    """District ViewSet"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch Districts"""
        officer = Officer.objects.get(user=request.user)
        districts = District.objects.filter(department=officer.department)
        districts = DistrictSerializer(districts, many=True)
        return sucess_response(districts.data)

    def post(self, request):
        """Add District"""
        officer = Officer.objects.get(user=request.user)
        name = request.data.get("name")
        district = District(name=name, department=officer.department)
        district.save()
        district = DistrictSerializer(district)
        return sucess_response(district.data, 'District Added Successfully')

    def put(self, request, _pk):
        """Update District"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        name = request.data.get("name")
        try:
            district = District.objects.get(id=_pk)
            district.name = name
            district.save()
            district = DistrictSerializer(district)
            return sucess_response(district.data, 'District Update Successfully')
        except District.DoesNotExist:
            return not_found_error('District Not Found')


    def delete(self, request, _pk):
        """Delete District"""
        try:
            officer = Officer.objects.get(user=request.user)
        except Officer.DoesNotExist:
            return not_found_error("Officer Not Found")
        try:
            district = District.objects.get(id=_pk)
            district.delete()
            return sucess_response(None, 'District Deleted  Successfully')
        except District.DoesNotExist:
            return not_found_error('District Not Found')
