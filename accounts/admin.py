"""Accounts Admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from api.utils import export_data_to_pdf
from .models import User, Officer, Log

# Register your models here.


class DepartmentFilter(SimpleListFilter):
    """Department filter"""
    title = 'department'
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        """ fetch all departments in admin_model"""
        departments = {c.department for c in model_admin.model.objects.all()}
        return [(c.id, c.name) for c in departments]

    def queryset(self, request, queryset):
        """ method to filter department"""
        if self.value():
            return queryset.filter(department__id__exact=self.value())
        return None


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Setup users admin page"""
    fieldsets = (
        (None, {'fields': ('email', 'password', 'profile_pic')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'groups', 'profile_pic'),
        }),
    )
    list_display = ('id', 'email', )
    search_fields = ['email', 'id']
    ordering = ('id', 'email',)


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    """Officer admin"""
    list_filter = (DepartmentFilter,)
    list_display = ('id', 'user', 'department', 'link', 'export_button')
    search_fields = ['first_name', 'last_name', 'id', 'badge_number', 'user__email']
    readonly_fields = ('link',)

    def get_urls(self):
        """fetch custom urls for all officers"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:officer_id>/export/',
                self.admin_site.admin_view(self.export_survey),
                name='survey-officer-export',
            )
        ]
        return custom_urls + urls

    @classmethod
    def export_survey(cls, request, officer_id, *args, **kwargs):
        """export survey for specific officer"""
        officer = Officer.objects.get(pk=officer_id)
        return export_data_to_pdf(officer, None, None)

    @classmethod
    def export_button(cls, obj):
        """export button to export specific officer's survey"""
        return format_html(
            '<a class="button" href="{}">Export</a>&nbsp;',
            reverse('admin:survey-officer-export', args=[obj.pk]),
        )
    export_button.short_description = 'Action'
    export_button.allow_tags = True


admin.site.register(Log)
