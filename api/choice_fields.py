from django.db import models


class Dispostion(models.TextChoices):
    arrested = 'Arrested'
    not_arrested = 'Not Arrested'


class Citizen_Ship(models.TextChoices):
    victom = 'victom'
    non_victom = 'non-victom'
    Subject = 'Subject'
    Caller = 'Caller'
    Witness = 'Witness'
    Suspect = 'Suspect'


class Category_Survey(models.TextChoices):
    Citizen_Police_Academy_Survey = 'Citizen_Police_Academy'
    Community_Engagement_Survey = 'Community_Engagement'
    Crime_Survey = 'Crime'
    Police_Public_Contract_Survey = 'Police_Public_Contact'
    Public_Safety_Survey = 'Public_Safety'
    Community_Pulse_Survey = 'Community_Pulse'
    Resident_Statisfaction_Survey = 'Resident_Statisfaction'
    Small_Business_Survey = 'Small_Buisness'
    School_Safety_Survey = 'School_Safety'
    Everything_Else = 'Everything'


class Category_Employee(models.TextChoices):
    Recuirment_Survey = 'Recuirment'
    Pre_Employment_Survey = 'Pre-Employment'
    onboarding_Survey = 'Onboarding'
    Traning_Survey = 'Traning'
    Pulse_Survey = 'Pulse'
    Employee_Satisfaction_Survey = 'Employee'
    Organizational_Survey = 'Organizational'
    Exit_Survey = 'Exit'
    Mental_Health_Survey = 'Mental'
    Police_Academy_Traning_Survey = 'Police'
    Everything_Else = 'Everything'
