"""Auth Related ViewSet"""
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from api.serializers import DetailOfficerSerializer
from accounts.models import Officer, ResetCode, User
from api.utils import sucess_response, not_found_error, send_reset_password_email


# Create your views here.
class TestViewSet(APIView):
    """Test View Set"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Return Hello World"""
        return sucess_response(None, 'Hello, World!')

class LoginViewSet(APIView):
    """Login View Set"""
    def post(self, request):
        """Login Api For Users"""
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        email = email.lower()
        if email is None:
            return not_found_error('Email should not be empty')
        if password is None:
            return not_found_error('Password should not be empty')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return not_found_error('User does not exist')

        user = authenticate(username=email, password=password)
        if user is not None:
            officer = Officer.objects.get(user=user)
            if officer.department.is_suspend == False:
                officer = DetailOfficerSerializer(officer)
                refresh = RefreshToken.for_user(user)
                content = {
                    'success': True,
                    'message': '',
                    'data': officer.data,
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
                return Response(content)
            else:
                return not_found_error('Account is suspended, contact the support for more detail')
        else:
            return not_found_error('Invalid login credentials')

class MeViewSet(APIView):
    """Me View Set"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """Fetch Current User"""
        officer = Officer.objects.get(user=request.user)
        officer_serializer = DetailOfficerSerializer(officer)
        return sucess_response(officer_serializer.data, '')

class LogoutViewSet(APIView):
    """Logout View Set"""
    def post(self, request):
        """Api To Add Token In BlackList"""
        token = request.data.get("refresh_token")
        token = RefreshToken(token)
        token.blacklist()
        return sucess_response(None, 'Logout Successfull')

class ResetPasswordViewSet(APIView):
    """Reset Password ViewSet"""
    def post(self, request):
        """Send Reset Code In Email"""
        email = request.data.get("email")
        email = email.lower()
        officer = None
        reset_code = None
        try:
            officer = Officer.objects.get(user__email=email)
        except Officer.DoesNotExist:
            return not_found_error('No account found with this email')
        try:
            reset_code = ResetCode.objects.get(officer=officer)
            reset_code.code = uuid.uuid4().hex[:6].upper()
            reset_code.save()
        except ResetCode.DoesNotExist:
            reset_code = ResetCode(
                officer=officer,
                code=uuid.uuid4().hex[:6].upper()
            )
            reset_code.save()
        send_reset_password_email(email, reset_code.code)
        return sucess_response(None, 'Reset Code is sent to your Email')

class SetNewPasswordViewSet(APIView):
    """Set NewPassword ViewSet"""
    def post(self, request):
        """Update Password"""
        code = request.data.get("code")
        password = request.data.get("password")
        email = request.data.get("email")
        email = email.lower()
        officer = None
        try:
            officer = Officer.objects.get(user__email=email)
        except Officer.DoesNotExist:
            return not_found_error('No account found with this email')
        try:
            ResetCode.objects.get(officer=officer, code=code)
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return sucess_response(None, 'Password Updated Successfully')
        except ResetCode.DoesNotExist:
            return not_found_error('Code Incoorect')
