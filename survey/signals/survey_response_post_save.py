from accounts.models import Officer
from api.utils import send_review_email, send_request_change_email, send_request_approved_email
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import SurveyResponse
import threading

class AddSurveyResponseThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(AddSurveyResponseThread, self).__init__(**kwargs)

    def run(self):
        send_review_email("A review has been left by " + self.instance.get_name(),
        "", self.instance.officer.user.email)
        supervisors = Officer.objects.filter(department=self.instance.officer.department, is_supervisor = True)
        for supervisor in supervisors:
            send_review_email("A review has been left for " + self.instance.officer.get_name(),
            "", supervisor.user.email)
        pass


class UpdateSurveyResponseThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(UpdateSurveyResponseThread, self).__init__(**kwargs)

    def run(self):
        if self.instance.changed_by_supervisor:
            officer = Officer.objects.get(id=self.instance.officer.id)
            subject = "Supervisor has update your feedback"
            send_request_approved_email(subject, self.instance.change_reason, officer.user.email)
        elif self.instance.request_change:
            supervisors = Officer.objects.filter(department=self.instance.officer.department, is_supervisor=True)
            subject = self.instance.officer.get_name() + "(" + self.instance.officer.badge_number +") request to change a feedback"
            for supervisor in supervisors:
                send_request_change_email(subject, self.instance.comment_reason, supervisor.user.email)
        pass



@receiver(post_save, sender=SurveyResponse)
def post_save_signal(sender,instance=None, created=False, **kwargs):
    if created:
        AddSurveyResponseThread(instance).start()
    else:
        UpdateSurveyResponseThread(instance).start()


