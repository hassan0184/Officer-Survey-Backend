from django.db import models
from api.utils import create_new_ref_number
from api.choice_fields import Dispostion, Citizen_Ship
from django.utils.translation import ugettext_lazy as _


class EventTypes(models.Model):
    '''Event type model to store event type instances '''
    department = models.ForeignKey(
        'department.Department', on_delete=models.CASCADE, related_name="eventtype_departments")
    eventtype = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")
        unique_together = ('department', 'eventtype',)

    def __str__(self) -> str:
        return self.eventtype


class SmsSurvey(models.Model):
    '''SmsSurvey model to store data related to events'''
    dispostion = models.CharField(
        choices=Dispostion.choices, default=Dispostion.arrested, max_length=50)
    citizen_ship = models.CharField(
        default=Citizen_Ship.victom, max_length=50)
    event_name = models.CharField(max_length=100)
    eventtype = models.ForeignKey(
        EventTypes, on_delete=models.CASCADE, related_name="events")
    department = models.ForeignKey(
        'department.Department', on_delete=models.CASCADE, related_name="events_department")
    from_field = models.CharField(max_length=200, default='')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Sms Survey")
        verbose_name_plural = _("Sms Surveys")

    def __str__(self) -> str:
        return self.event_name


class MessageSendData(models.Model):
    '''MessageSend model to store message instances'''
    department = models.ForeignKey(
        'department.Department', on_delete=models.CASCADE, related_name="message_departments")
    user_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)

    refrence = models.CharField(
        max_length=5,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_ref_number
    )
    is_clicked = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Message Send")
        verbose_name_plural = _("Messages Send")

    def __str__(self) -> str:
        return self.user_name


class DatabaseDepartments(models.Model):
    """model to store sms-survey databaase"""
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    database = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    department = models.ForeignKey(
        'department.Department', on_delete=models.CASCADE, related_name="departments_database")

    class Meta:
        verbose_name = _("Department Database")
        verbose_name_plural = _("Departments Databases")
