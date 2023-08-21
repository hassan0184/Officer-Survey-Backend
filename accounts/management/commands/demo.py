import os
from django.core.management.base import BaseCommand
from accounts.models import User
from department.models import *
from survey.models import *
from accounts.models import *
import datetime
import random

password = "@fficer$urvey12"

first_name_list = [
    'Tony',
    'Jericho',
    'Alex',
    'Julia',
    'Lauren',
    'Pete',
    'John',
    'Carlos',
    'Kevin',
    'Jonathan',
    'Ryan',
    'Jenny',
    'Lori',
    'Rebecca',
    'Laura',
    'Joan',
    'Steve',
    'Kathy',
    'Frank',
    'Lindsey'
]

last_name_list = [
    'Malik',
    'Williams',
    'Moore',
    'Watson',
    'Alex',
    'Smith',
    'Doe',
    'Gomez',
    'Matthew',
    'Vilma',
    'Victors',
    'Smith',
    'Gooding',
    'Lockheed',
    'Martin',
    'Jackson',
    'Hamilton',
    'Wallace',
    'Tilley',
    'Patrick'
]

city_with_zip_code_list =[
   {
       "City": "St. Louis",
       "State": "Missouri",
       "Zip Code": "63136"
    },
    {
        "City": "Chicago",
        "State": "Illinois",
        "Zip Code": "60007"
    },
    {
        "City": "Los Angeles",
        "State": "Louisiana",
        "Zip Code": "90222"
    },
    {
        "City": "NY",
        "State": "New York",
        "Zip Code": "10001"
    },
    {
        "City": "Frederick",
        "State": "Maryland",
        "Zip Code": "21776"
    },
    {
        "City": "Washington ",
        "State": "D.C.",
        "Zip Code": "20002"
    },
    {
        "City": "St. Louis",
        "State": "Missouri",
        "Zip Code": "63136"
    },
    {
        "City": "St. Louis",
        "State": "Missouri",
        "Zip Code": "63138"
    },
    {
        "City": "St. Charles",
        "State": "Missouri",
        "Zip Code": "63303"
    },
    {
        "City": "Dallas",
        "State": "Texas",
        "Zip Code": "78781"
    },
    {
        "City": "Denver",
        "State": "Colorado",
        "Zip Code": "80014"
    },
    {
        "City": "Phoenix",
        "State": "Arizona",
        "Zip Code": "850001"
    },
    {
        "City": "Austin",
        "State": "Texas",
        "Zip Code": "78781"
    },
    {
        "City": "Seattle",
        "State": "Washington",
        "Zip Code": "98101"
    },
    {
        "City": "Cleveland ",
        "State": "Ohio",
        "Zip Code": "44101"
    },
    {
        "City": "Cleveland ",
        "State": "Ohio",
        "Zip Code": "44101"
    },
    {
        "City": "Miami",
        "State": "Florida",
        "Zip Code": "33101"
    },
    {
        "City": "Jacksonville",
        "State": "Florida",
        "Zip Code": "33889"
    },
    {
        "City": "Atlanta",
        "State": "Georgia",
        "Zip Code": "30301"
    },
    {
        "City": "Cheyenne",
        "State": "Wyoming",
        "Zip Code": "82001"
    }
]

address_list = [
    '6002 Demo Street',
    '555 Downtown Street',
    '123 Main Street',
    '222 Main Street',
    '76 Opserway Drive',
    '9001 NE Street',
    '5549 Rock Road',
    '5549 Rock Road',
    '3890 Hello Street',
    '7732 Dallas Drive',
    '27893 Guthrie Road',
    '2378 Arizona Drive',
    '28934 Austin Street',
    '27893 Seattle Blvd',
    '9018 Pear Street',
    '9018 Pear Steet',
    '2830 Carlos Street',
    '7829 Jackson Street',
    '4569 Peachstreet',
    '7822 Sheriff Street'
]


comment_box_list = [
    'You are just fine',
    'No',
    'Yes, Officer should be polite.'
]

comment_box_of_question_list = [
    '',
    'No',
    'Yes'
]

officer_list = [
    {
        "First Name": "Tony",
        "Last Name": "Malik",
        "Badge Number": "8093",
        "Address": "6002 Demo Street",
        "City": "St. Louis",
        "State": "Missouri",
        "Zip Code": "63136",
        "Phone Number": "314-215-9918",
        "Email": "tonymalik@outlook.com",
        "Profile Pic Name": "image-1.jpg"
    },
    {
        "First Name": "Jericho",
        "Last Name": "Williams",
        "Badge Number": "7832",
        "Address": "555 Downtown Street",
        "City": "Chicago",
        "State": "Illinois",
        "Zip Code": "60007",
        "Phone Number": "618-999-0000",
        "Email": "officersurveyofficer@gmail.com",
        "Profile Pic Name": "image-2.jpg"
    },
    {
        "First Name": "Alex",
        "Last Name": "Moore",
        "Badge Number": "8903",
        "Address": "123 Main Street",
        "City": "Los Angeles",
        "State": "Louisiana",
        "Zip Code": "90222",
        "Phone Number": "310-992-3333",
        "Email": "amore99922@gmail.com",
        "Profile Pic Name": "image-3.jpg"
    },
    {
        "First Name": "Julia",
        "Last Name": "Watson",
        "Badge Number": "548",
        "Address": "222 Main Street",
        "City": "NY",
        "State": "New York",
        "Zip Code": "10001",
        "Phone Number": "212-939-0222",
        "Email": "juliawatsonishere33@gmail.com",
        "Profile Pic Name": "image-4.jpg"
    },
    {
        "First Name": "Lauren",
        "Last Name": "Alex",
        "Badge Number": "80",
        "Address": "76 Opserway Drive",
        "City": "Frederick",
        "State": "Maryland",
        "Zip Code": "21776",
        "Phone Number": "301-393-9939",
        "Email": "laurenmalik0409@outlook.com",
        "Profile Pic Name": "image-5.jpg"
    },
    {
        "First Name": "Pete",
        "Last Name": "Smith",
        "Badge Number": "2929",
        "Address": "9001 NE Street",
        "City": "Washington ",
        "State": "D.C.",
        "Zip Code": "20002",
        "Phone Number": "202-777-000",
        "Email": "petesmith88833@hotmail.com",
        "Profile Pic Name": "image-6.jpg"
    },
    {
        "First Name": "John",
        "Last Name": "Doe",
        "Badge Number": "8093",
        "Address": "5549 Rock Road",
        "City": "St. Louis",
        "State": "Missouri",
        "Zip Code": "63136",
        "Phone Number": "314-990-9999",
        "Email": "johndoeisherepd@gmail.com",
        "Profile Pic Name": "image-7.jpg"
    },
    {
        "First Name": "Carlos",
        "Last Name": "Gomez",
        "Badge Number": "7832",
        "Address": "5549 Rock Road",
        "City": "St. Louis",
        "State": "Missouri",
        "Zip Code": "63138",
        "Phone Number": "314-990-9999",
        "Email": "gomezcarlos883332@gmail.com",
        "Profile Pic Name": "image-8.jpg"
    },
    {
        "First Name": "Kevin",
        "Last Name": "Matthew",
        "Badge Number": "6630",
        "Address": "3890 Hello Street",
        "City": "St. Charles",
        "State": "Missouri",
        "Zip Code": "63303",
        "Phone Number": "636-992-0092",
        "Email": "mkiklkd747@hotmail.com",
        "Profile Pic Name": "image-9.jpg"
    },
    {
        "First Name": "Jonathan ",
        "Last Name": "Vilma",
        "Badge Number": "4109",
        "Address": "7732 Dallas Drive",
        "City": "Dallas",
        "State": "Texas",
        "Zip Code": "78781",
        "Phone Number": "660-990-0099",
        "Email": "iamdallaspd22228H@hotmail.com",
        "Profile Pic Name": "image-10.jpg"
    },
    {
        "First Name": "Ryan",
        "Last Name": "Victors",
        "Badge Number": "9099",
        "Address": "27893 Guthrie Road",
        "City": "Denver",
        "State": "Colorado",
        "Zip Code": "80014",
        "Phone Number": "660-990-0099",
        "Email": "rvictors$$2321@gmail.com",
        "Profile Pic Name": "image-11.jpg"
    },
    {
        "First Name": "Jenny",
        "Last Name": "Smith",
        "Badge Number": "8388",
        "Address": "2378 Arizona Drive",
        "City": "Phoenix",
        "State": "Arizona",
        "Zip Code": "850001",
        "Phone Number": "770-993-9320",
        "Email": "jsmithing22290@hotmail.com",
        "Profile Pic Name": "image-12.jpg"
    },
    {
        "First Name": "Lori",
        "Last Name": "Gooding",
        "Badge Number": "7720",
        "Address": "28934 Austin Street",
        "City": "Austin",
        "State": "Texas",
        "Zip Code": "78781",
        "Phone Number": "990-221-9912",
        "Email": "lorismithing4411$@gmail.com",
        "Profile Pic Name": "image-13.jpg"
    },
    {
        "First Name": "Rebecca",
        "Last Name": "Lockheed",
        "Badge Number": "6621",
        "Address": "27893 Seattle Blvd",
        "City": "Seattle",
        "State": "Washington",
        "Zip Code": "98101",
        "Phone Number": "773-040-0039",
        "Email": "rlokcked31red@yahoo.com",
        "Profile Pic Name": "image-14.jpg"
    },
    {
        "First Name": "Laura",
        "Last Name": "Martin",
        "Badge Number": "1120",
        "Address": "9018 Pear Street",
        "City": "Cleveland ",
        "State": "Ohio",
        "Zip Code": "44101",
        "Phone Number": "889-002-9377",
        "Email": "lmartin22!fox@att.net",
        "Profile Pic Name": "image-15.jpg"
    },
    {
        "First Name": "Joan",
        "Last Name": "Jackson",
        "Badge Number": "3381",
        "Address": "9018 Pear Steet",
        "City": "Cleveland ",
        "State": "Ohio",
        "Zip Code": "44101",
        "Phone Number": "889-002-2999",
        "Email": "jjknowsbest22922222@att.net",
        "Profile Pic Name": "image-16.jpg"
    },
    {
        "First Name": "Steve",
        "Last Name": "Hamilton",
        "Badge Number": "1422",
        "Address": "2830 Carlos Street",
        "City": "Miami",
        "State": "Florida",
        "Zip Code": "33101",
        "Phone Number": "660-123-0099",
        "Email": "sha2miltontt22!@gmail.com",
        "Profile Pic Name": "image-17.jpg"
    },
    {
        "First Name": "Kathy",
        "Last Name": "Wallace",
        "Badge Number": "7728",
        "Address": "7829 Jackson Street",
        "City": "Jacksonville",
        "State": "Florida",
        "Zip Code": "33889",
        "Phone Number": "921-011-9111",
        "Email": "kwalllacehardwood222!@gmail.com",
        "Profile Pic Name": "image-18.jpg"
    },
    {
        "First Name": "Frank",
        "Last Name": "Patel",
        "Badge Number": "1200",
        "Address": "4569 Peachstreet",
        "City": "Atlanta",
        "State": "Georgia",
        "Zip Code": "30301",
        "Phone Number": "404-194-9334",
        "Email": "tilleyfrankyoutube3311@hotmail.com",
        "Profile Pic Name": "image-19.jpg"
    },
    {
        "First Name": "Lindsey ",
        "Last Name": "Patrick",
        "Badge Number": "3890",
        "Address": "7822 Sheriff Street",
        "City": "Cheyenne",
        "State": "Wyoming",
        "Zip Code": "82001",
        "Phone Number": "636-900-6112",
        "Email": "patricklindseylovesme21149@gmail.com",
        "Profile Pic Name": "image-20.jpg"
    }
]
class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Department.objects.filter(name='TestDepartment').exists():
            ### Adding Test Department ###
            survey = Survey.objects.filter(name="Sample Survey").first()

            if survey is None:
                survey = Survey.objects.create(name="Sample Survey" , about="123")

            department = Department(
                name="Test Department",
                address="9001 NE Street",
                city="Washington",
                state="D.C.",
                zip_code="20002",
                phone="202-777-000",
                survey=survey)
            department.save()

            list_district = []

            district = District(name="District 1", department=department)
            district.save()
            list_district.append(district)
            district = District(name="District 2", department=department)
            district.save()
            list_district.append(district)
            district = District(name="District 3", department=department)
            district.save()
            list_district.append(district)

            ### Adding Test Department Supervisor ###
            user =  User(email='officersurveysupervisor@gmail.com', profile_pic="image-1.jpg")
            user.set_password(password)
            supervisor = Officer(
                user= user,
                first_name= "Test",
                last_name= "Supervisor",
                phone="8189521996",
                badge_number = "54278",
                is_supervisor=True,
                department= department)
            user.save()
            supervisor.save()

            ### Adding Test Department Officer ###



            officers = []
            survey_responses = []
            for officer in officer_list:
                user =  User(
                    email=officer['Email'],
                    profile_pic=officer['Profile Pic Name']
                )
                user.set_password(password)
                officer = Officer(
                    user= user,
                    first_name= officer['First Name'],
                    last_name= officer['Last Name'],
                    badge_number= officer['Badge Number'],
                    address= officer['Address'],
                    city= officer['City'],
                    state= officer['State'],
                    zip_code= officer['Zip Code'],
                    department= department,
                    district=list_district[random.randint(0, len(list_district)-1)])
                user.save()
                officer.save()
                officers.append(officer)
                for x in range(random.randint(50, 100)):
                    date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 90), minutes=random.randint(1, 60),  hours=random.randint(1, 24))
                    city_with_zip_code_list_index = random.randint(0,len(city_with_zip_code_list)-1)
                    survey_response = SurveyResponse(
                        officer=officer,
                        survey=department.survey,
                        rating=random.randint(1,5),
                        first_name=first_name_list[random.randint(0,len(first_name_list)-1)],
                        last_name=last_name_list[random.randint(0,len(last_name_list)-1)],
                        zip_code=city_with_zip_code_list[city_with_zip_code_list_index]["Zip Code"],
                        city=city_with_zip_code_list[city_with_zip_code_list_index]["City"],
                        state=city_with_zip_code_list[city_with_zip_code_list_index]["State"],
                        address= address_list[random.randint(0,len(address_list)-1)]
                    )
                    survey_response.save()
                    survey_response.created_at = date
                    survey_response.save()
                    survey_responses.append(survey_response)
                    questions = Question.objects.filter(survey=department.survey)
                    for question in questions:
                        choices = Choice.objects.filter(question=question)
                        choice_answer = None
                        if len(choices) > 0:
                            choice_answer = choices[random.randint(0,len(choices)-1)]
                        comment_box =  ""
                        if question.type == "Text Area":
                            comment_box = comment_box_list[random.randint(0,len(comment_box_list)-1)]
                        elif choice_answer.show_comment_box:
                            comment_box = comment_box_of_question_list[random.randint(0,len(comment_box_of_question_list)-1)]
                        question_response = QuestionResponse(
                            survey = survey_response,
                            question = question,
                            choice = choice_answer,
                            comment_box = comment_box
                        )
                        question_response.save()
                        pass
                pass
            count = 50
            for x in range(count):
                index = random.randint(0, len(survey_responses) - 1)
                survey_response = survey_responses[index]
                survey_response.request_change = True
                survey_response.comment_reason = "Kindly update this review as I did my best but citizen was rude"
                change = range(random.randint(1, 4))
                if change == 2:
                    survey_response.changed_by_supervisor = True
                    survey_response.change_reason = "I have diged into issue and find out, officer was right, so updating the review"
                    survey_response.rating = 4
                survey_response.save()
                pass
            survey_responses = SurveyResponse.objects.filter(zip_code="98101")
            for survey_response in survey_responses:
                survey_response.rating = random.randint(4,5)
                survey_response.save()
                pass
            survey_responses = SurveyResponse.objects.filter(zip_code="60007")
            for survey_response in survey_responses:
                survey_response.rating = random.randint(2,4)
                survey_response.save()
                pass
            survey_responses = SurveyResponse.objects.filter(zip_code="30301")
            for survey_response in survey_responses:
                survey_response.rating = random.randint(1,2)
                survey_response.save()
                pass


