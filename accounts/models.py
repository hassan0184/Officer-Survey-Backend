"""User Model and some other Models"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from datetime import timedelta
import uuid

STATES = (
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('D.C', 'D.C'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('Indiana', 'Indiana'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
)


class User(AbstractUser):
    """Model to create user"""
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=40, unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    profile_pic = models.ImageField(default='profilePicture/default_profie_pic.png',
                                    upload_to='profilePicture')
    objects = UserManager()

    def __str__(self):
        """return email of user"""
        return self.email


class Officer(models.Model):
    """Model to create officer"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey("department.Department",
                                   on_delete=models.CASCADE)
    district = models.ForeignKey("department.District",
                                 on_delete=models.SET_NULL, null=True, blank=True)
    badge_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    link = models.CharField(max_length=10, editable=False, unique=True,
                            null=True, blank=True)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    is_supervisor = models.BooleanField(default=False)
    state = models.CharField(max_length=200, blank=True, choices=STATES)
    zip_code = models.CharField(max_length=200, blank=True)
    training = models.BooleanField(default=False)

    def __str__(self):
        """return first_name of officer"""
        return self.first_name

    def get_name(self):
        """get officer name"""
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        """Overide the save method of model class"""

        if self.link is None:
            self.link = uuid.uuid4().hex[:9].upper()

        return super(Officer, self).save(*args, **kwargs)


class Log(models.Model):
    """Model to get logged_supervisor and all logged_officer"""
    officer = models.ForeignKey(Officer,  on_delete=models.CASCADE, related_name='logged_officer')
    in_training = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    supervisor = models.ForeignKey(Officer, null=True,
                                   on_delete=models.SET_NULL, related_name='log_by_supervisor')


class ResetCode(models.Model):
    """Create reset code for password reset"""
    officer = models.OneToOneField(Officer, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)


class Notes(models.Model):
    """Model for making notes for officer"""
    notes_by = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name="notes_by")
    created_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=1000, blank=True)
    notes_for = models.ForeignKey(Officer, on_delete=models.CASCADE,
                                  null=True, related_name="notes_for")

    def get_notes_date(self, hours):
        """Fetch Notes of Dates"""
        created_at = self.created_at
        if hours is not None:
            created_at = created_at + timedelta(minutes=int(hours))
        return created_at.strftime("%Y-%m-%d, %H:%M:%S")
