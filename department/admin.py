"""Department Admin"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from api.utils import export_department_data_to_pdf
from .models import Department, District, Support

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Department Admin"""
    list_display = ('id', 'name', 'export_button' )
    search_fields = ['name', 'id']

    def get_urls(self):
        """fetch custom urls for all departments"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:department_id>/export/',
                self.admin_site.admin_view(self.export_survey),
                name='survey-export',
            )
        ]
        return custom_urls + urls

    @classmethod
    def export_survey(cls, request, department_id, *args, **kwargs):
        """export survey for specific department"""
        department = Department.objects.get(pk=department_id)
        return export_department_data_to_pdf(department)

    @classmethod
    def export_button(cls, obj):
        """export button to export specific officer's department"""
        return format_html(
            '<a class="button" href="{}">Export</a>&nbsp;',
            reverse('admin:survey-export', args=[obj.pk]),
        )
    export_button.short_description = 'Action'
    export_button.allow_tags = True
admin.site.register(District)
admin.site.register(Support)
