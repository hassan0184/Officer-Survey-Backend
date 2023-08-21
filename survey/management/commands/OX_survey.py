from django.core.management.base import BaseCommand
from survey.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Survey.objects.filter(name="OX").exists():
            survey = Survey(
                name="OX",
                about="Please take a moment and complete the survey based on today’s experience. Your survey will help us improve our Police Department and understand our community better."
            )
            survey.save()
            ###Q1###
            question = Question(
                question="Was the officer polite and professional?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="No",
                show_comment_box=True,
                comment_box_place_holder="If not, please provide more information below.",
                question=question
            )
            choice.save()
            ###Q2###
            question = Question(
                question="Did the officer listen to your concern?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="No",
                show_comment_box=True,
                comment_box_place_holder="If not, please provide more information below.",
                question=question
            )
            choice.save()
            ###Q3###
            question = Question(
                question="Did the officer explain ways to resolve the issue?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="No",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="N/A",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()

            ###Q4###
            question = Question(
                question="Did the officer treat you fairly during the encounter?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="No",
                show_comment_box=True,
                comment_box_place_holder="If not, please provide more information below.",
                question=question
            )
            choice.save()
            ###Q5###
            question = Question(
                question="Are there any comments you would like to leave?",
                type="Text Area",
                survey=survey
            )
            question.save()
