from django.db.models.signals import post_save
from django.db.models import Q
from django.contrib.auth.models import User
from django.dispatch import receiver
from ..models import Question, QuestionTranslation, LANGUAGE_CHOICES, translate_text
import threading

class QuestionThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(QuestionThread, self).__init__(**kwargs)

    def run(self):
        is_new = False
        if self.instance.id == None:
            is_new=True
        if is_new:
            for key in LANGUAGE_CHOICES:
                question_trans = QuestionTranslation(text=translate_text(self.instance.question, key[0]), language=key[0], question=self.instance)
                question_trans.save()
        else:
            for key in LANGUAGE_CHOICES:
                try:
                    question_trans = QuestionTranslation.objects.get(Q(language=key[0]) & Q(question=self.instance))
                    question_trans.text = translate_text(self.instance.question, key[0])
                    question_trans.save()
                except QuestionTranslation.DoesNotExist:
                    question_trans = QuestionTranslation(text=translate_text(self.instance.question, key[0]), language=key[0], question=self.instance)
                    question_trans.save()

@receiver(post_save, sender=Question)
def post_save_signal(sender,instance=None, **kwargs):
    QuestionThread(instance).start()


