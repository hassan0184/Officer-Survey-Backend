"""Events related viewset"""
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveDestroyAPIView, UpdateAPIView, CreateAPIView
from accounts.models import Officer
from department.models import Department
from events.models import SmsSurvey, EventTypes, MessageSendData
from api.serializers import MessageSendDataSerializer, SmsSurveySerializer, CreateSmsSurveySerializer, EventTypeSerializer, SmsSurveyDetailSerializer, SmsSurveyUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import django_filters
from api.utils import (sucess_response, bad_request_error)


class SmsSurveyListApiView(ListAPIView):
    """Filter SmsSurvey on departments  """
    permission_classes = [IsAuthenticated]
    model = SmsSurvey
    serializer_class = SmsSurveyDetailSerializer
    queryset = SmsSurvey.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ('department',)


class SendMessageData(ListAPIView):
    """Filter to get sms messages sended to Department"""
    model = MessageSendData
    serializer_class = MessageSendDataSerializer
    queryset = MessageSendData.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ('department',)


class SmsSurveyUpdateView(UpdateAPIView):
    """this create crud for Sms survey"""
    permission_classes = [IsAuthenticated]
    serializer_class = SmsSurveyUpdateSerializer
    queryset = SmsSurvey.objects.all()


class SmsSurveyview(RetrieveDestroyAPIView):
    """this create crud for sms Survey"""
    permission_classes = [IsAuthenticated]
    serializer_class = SmsSurveySerializer
    queryset = SmsSurvey.objects.all()


class CreateSmsSurvey(CreateAPIView):
    """post api for sms survey"""
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSmsSurveySerializer
    queryset = SmsSurvey.objects.all()


class EventTypeListApiView(ListAPIView):
    """filter Event Type on departments """
    permission_classes = [IsAuthenticated]
    model = EventTypes
    serializer_class = EventTypeSerializer
    queryset = EventTypes.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ('department',)


class EventTypeview(RetrieveUpdateDestroyAPIView):
    """this create crud for Eventtype"""
    permission_classes = [IsAuthenticated]
    serializer_class = EventTypeSerializer
    queryset = EventTypes.objects.all()


class CreateEventType(APIView):
    """Create Event Type"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Department.objects.get(id=request.data['department'])
            obj = EventTypeSerializer(data=request.data)
            if obj.is_valid():
                obj.save()
                return Response(obj.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MessageSendview(APIView):
    """Api to fetch Messages stats"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            department = self.request.GET.get('department', None)
            start_date = self.request.GET.get('start_date', None)
            end_date = self.request.GET.get('end_date', None)
            data = MessageSendData.objects.filter(
                date__range=[start_date, end_date], department=department)
            message = MessageSendDataSerializer(data, many=True)
            return Response({"messages": message.data, "messages_count": data.count()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadEventJsonViewSet(APIView):
    """Upload Officers ViewSet"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """events to be added from json"""
        try:
            data = dict()
            data = request.data
            events = [event["eventtype"] for event in data]
            officer = Officer.objects.get(user=request.user.id)
            department = Department.objects.get(id=officer.department.id)
            for eventtype in events:
                if EventTypes.objects.filter(eventtype__iexact=eventtype).first() is None:
                    event = EventTypes(department=department,
                                       eventtype=eventtype)
                    event.save()
            return sucess_response(None, 'All events  Added Successfully')
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateMessageSendData(APIView):
    "UPDATE click count for event"

    permission_classes = [AllowAny]

    def patch(self, request):
        '''patch api to update message instance'''
        ref = request.data.pop('ref', None)
        if ref is None:
            return bad_request_error("ref required in body")
        message = MessageSendData.objects.filter(refrence=ref).first()
        if message is None:
            return bad_request_error("message instance wit this refrence code does not exist")

        serializer = MessageSendDataSerializer(
            message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return sucess_response(serializer.data, "updated successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
