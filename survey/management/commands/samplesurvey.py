import os
from django.core.management.base import BaseCommand
from survey.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Survey.objects.filter(name="Sample Survey").exists():
            survey = Survey(
                name="Sample Survey",
                about="Please take a moment and complete the survey based on today’s experience. Your survey will help us improve our Police Department and understand our community better."
            )
            survey.save()
            ###Q1###
            question = Question(
                question="Were you treated professionally, with dignity and respect?",
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
                question="Did the officer(s) arrive in a timely manner?",
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
                comment_box_place_holder="If not, please provide approximate time it took the officer(s) to arrive.",
                question=question
            )
            choice.save()
            ###Q3###
            question = Question(
                question="What was the reasoning for the call / stop?",
                type="Drop Down",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="911",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Abandon  Vehicle",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Aircraft Crash",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Animal Abuse",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Animal Compliant ",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Arson",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Assault all types",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Assist Citizen ",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Attempt to Locate",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Audible Alarm",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Automobile Accident - all types",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="BOMB Threat",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Burglary - all types",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Business Burglary",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Citizen Contact",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Dead Body",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Domestic Disturbance",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Drowning",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="DWI / DUI",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Extra Patrol Request",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Fight in Progress",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Fire Alarm",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Fireworks compliant",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Found Property",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Fraud",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Harassment",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Hazard",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Hit and Run Pedestrian",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Hold Up / Robbery Alarm",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Indecent Exposure ",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Juvenile Abuse",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Kidnapping",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Larcency",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Littering / Dumping",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Loud Music",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Mental illness",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Minor in Possession of Alcohol / Drugs",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Missing Juvenile",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Missing Person",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Motor Assist",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Noise Complaint ",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Ordinance Violation",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Panic Alarm",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Parking Compliant",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Peach Distrubance",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Prowler",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Recovered Stolen Vehicle",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Robbery",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Security Check",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Sex Crimes",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Shooting",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Shoplifter",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Shots Fire",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Sick Case",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Silent Alarm",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Stand by to keep the peace",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Stolen Vehicle Just Occured",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Suspicious Persons",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Suspicious Vehicle",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Theft",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Theft from Vehicle",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Traffic Stop",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Trespass",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Vacation Check",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Weapons Violation",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Welfare Check",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Other",
                show_comment_box=True,
                comment_box_place_holder="Specify the Reason",
                question=question
            )
            choice.save()
            ###Q4###
            question = Question(
                question="Were there multiple officers on the scene? If so, provide their names below",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=True,
                comment_box_place_holder="If yes, please provide other Officers names if available.",
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
            ###Q5###
            question = Question(
                question="Did the officer solve your concern and / or provide you with proper information?",
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
            ###Q6###
            question = Question(
                question="Would you like a supervisor to call or email you about today’s situation?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Yes",
                show_comment_box=True,
                comment_box_place_holder="If yes, enter your telephone number and/or email where you can be reached.",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="No",
                show_comment_box=False,
                comment_box_place_holder="If not, please provide more information below.",
                question=question
            )
            choice.save()
            ###Q7###
            question = Question(
                question="What is your race?",
                type="Drop Down",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="African American",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="White",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Hispanic",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Asian",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="American Indian",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Native Hawaiian or Other Pacific Islander",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Other",
                show_comment_box=True,
                comment_box_place_holder="Please specify your race.",
                question=question
            )
            choice.save()
            ###Q8###
            question = Question(
                question=" What is your age group?",
                type="Drop Down",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="18-24",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="25-34",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="35-44",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="45-54",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="55-64",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="65+",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            ###Q9###
            question = Question(
                question="What is your gender?",
                type="Drop Down",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Male",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Female",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Other",
                show_comment_box=True,
                comment_box_place_holder="Please specify your gender.",
                question=question
            )
            choice.save()

            ###Q10###
            question = Question(
                question="Overall, how well do you feel our Police Department does, in providing services to the community?",
                type="Multiple Choice",
                survey=survey
            )
            question.save()
            choice = Choice(
                choice="Great",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Average",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            choice = Choice(
                choice="Needs Improvement",
                show_comment_box=False,
                comment_box_place_holder="",
                question=question
            )
            choice.save()
            ###Q11###
            question = Question(
                question="How can we improve?",
                type="Text Area",
                survey=survey
            )
            question.save()
            ###Q12###
            question = Question(
                question="Is there anything else you’d like to add?",
                type="Text Area",
                survey=survey
            )
            question.save()






