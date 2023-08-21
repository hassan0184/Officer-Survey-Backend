from django.db.models.signals import post_save
from django.db.models import Q
from django.contrib.auth.models import User
from django.dispatch import receiver
from ..models import Choice, LANGUAGE_CHOICES, translate_text, ChoiceTranslation
import threading
class ChoiceThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(ChoiceThread, self).__init__(**kwargs)

    def run(self):
        is_new = False
        if self.instance.id == None:
            is_new=True
        if is_new:
            for key in LANGUAGE_CHOICES:
                choice_trans = ChoiceTranslation(text=translate_text(self.instance.choice, key[0]), language=key[0], choice=self.instance)
                choice_trans.save()
        else:
            for key in LANGUAGE_CHOICES:
                try:
                    choice_trans = ChoiceTranslation.objects.get(Q(language=key[0]) & Q(choice=self.instance))
                    choice_trans.text = translate_text(self.instance.choice, key[0])
                    choice_trans.save()
                except ChoiceTranslation.DoesNotExist:
                    choice_trans = ChoiceTranslation(text=translate_text(self.instance.choice, key[0]), language=key[0], choice=self.instance)
                    choice_trans.save()

@receiver(post_save, sender=Choice)
def post_save_signal(sender,instance=None, **kwargs):
    ChoiceThread(instance).start()
