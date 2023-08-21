from django.core import validators
from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class LatitudeLongitude(models.Model):
    ''' Model create zip_code table '''
    latitude = models.CharField(max_length = 25, blank = True)
    longitude = models.CharField(max_length = 25, blank = True)
    zip_code = models.CharField(max_length = 11, unique = True, validators=[RegexValidator(regex = '[0-9]{5}(-[0-9]{5})?',message = 'Zip Code is not valid')])

    def __str__(self):
        '''default get method to return latitude longitude and zip code'''
        return 'Zip Code :' + self.zip_code + '\t Latitude :' + self.latitude + '\tLongitude :' + self.longitude