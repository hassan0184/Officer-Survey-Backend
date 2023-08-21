from django.contrib import admin
from miscellaneous.models import LatitudeLongitude
# Register your models here.

@admin.register(LatitudeLongitude)
class LatitudeLongitudeAdmin(admin.ModelAdmin):
    list_display = ['zip_code', 'latitude', 'longitude']
