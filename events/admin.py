from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from events.models import MessageSendData, EventTypes, SmsSurvey, DatabaseDepartments


@admin.register(MessageSendData)
class MessageSendDataAdmin(admin.ModelAdmin):
    """Register MessageSendData in Admin"""
    list_filter = ('department', ('date', DateRangeFilter),
                   'is_clicked', 'is_submitted',)
    list_display = ('department', 'event_type', 'date', 'refrence',)


admin.site.register(EventTypes)
admin.site.register(SmsSurvey)
admin.site.register(DatabaseDepartments)
