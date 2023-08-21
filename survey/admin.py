"""Create Filtering classes and register some models them in Admin"""
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import (ChoiceTranslation, Question, QuestionTranslation, Survey,
                     QuestionResponse, Choice, SurveyResponse, Employee360Survey, Employee360Question, Employee360Choice,
                     Employee360SurveyResponse, Employee360QuestionResponse, CommunitySurvey,
                     CommunityQuestion, CommunityChoice, CommunityQuestionResponse, CommunitySurveyResponse, CallBack)


class SurveyFilter(SimpleListFilter):
    """Survey Filter"""
    title = 'survey'
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        """fetch survey in admin_model"""
        surveys = {c.survey for c in model_admin.model.objects.all()}
        return [(c.id, c.name) for c in surveys]

    def queryset(self, request, queryset):
        """method to filter survey"""
        if self.value():
            return queryset.filter(survey__id__exact=self.value())
        return None


class SurveyResponseFilter(SimpleListFilter):
    """Survey Response Filter"""
    title = 'survey'
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        """fetch survey with specific date in admin_model"""
        surveys = {c.survey for c in model_admin.model.objects.all()}
        return [(c.id,  c.survey.name + " -" + str(c.created_at)) for c in surveys]

    def queryset(self, request, queryset):
        """method to filter survey"""
        if self.value():
            return queryset.filter(survey__id__exact=self.value())
        return None


class QuestionFilter(SimpleListFilter):
    """Question Filter"""
    title = 'question'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        """fetch question with survey in admin_model"""
        questions = {c.question for c in model_admin.model.objects.all()}
        return [(c.id, str(c.id) + " - " + c.survey.name) for c in questions]

    def queryset(self, request, queryset):
        """method to filter question"""
        if self.value():
            return queryset.filter(question__id__exact=self.value())
        return None


class QuestionResponseFilter(SimpleListFilter):
    """Question Response Filter"""
    title = 'question'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        """fetch question with survey in admin_model"""
        questions = {c.question for c in model_admin.model.objects.all()}
        return [(c.id, str(c.id) + " - " + c.survey.name) for c in questions]

    def queryset(self, request, queryset):
        """method to filter question"""
        if self.value():
            return queryset.filter(question__id__exact=self.value())
        return None


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """Register Survey in Admin"""
    list_display = ('id', 'name', 'about')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Register Question in Admin"""
    list_filter = (SurveyFilter,)
    list_display = ('id', 'question', 'type', 'survey', 'order')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Register Choice in Admin"""
    list_filter = (QuestionFilter,)
    list_display = ('id', 'choice', 'show_comment_box')


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    """Register SurveyResponse in Admin"""
    list_filter = (SurveyFilter,)
    list_display = ('id', 'first_name', 'last_name', 'rating', 'created_at')
    search_fields = ['zip_code', 'city', 'id', 'state', 'officer__user__email']


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    """Register QuestionResponse in Admin"""
    # list_filter = (SurveyResponseFilter,)
    list_display = ('id', 'question', 'choice')
    search_fields = ['survey__id', 'id']


class Employee360SurveyResponseFilter(SimpleListFilter):
    """Employee360 Survey Response Filter"""
    title = 'survey'
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        """fetch surveys in admin_model"""
        surveys = {c.survey for c in model_admin.model.objects.all()}
        return [(c.id, c.title) for c in surveys]

    def queryset(self, request, queryset):
        """method to filter survey"""
        if self.value():
            return queryset.filter(survey__id__exact=self.value())
        return None


@admin.register(Employee360SurveyResponse)
class Employee360SurveyResponseAdmin(admin.ModelAdmin):
    """Register Employee360SurveyResponse in Admin"""
    list_filter = (Employee360SurveyResponseFilter,)
    list_display = ('id', 'survey', 'created_at')


class Employee360QuestionResponseResponseFilter(SimpleListFilter):
    """Employee360 QuestionResponse ResponseFilter"""
    title = 'survey'
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        """fetch surveys with date in admin_model"""
        surveys = {c.survey for c in model_admin.model.objects.all()}
        return [(c.id, str(c.survey) + '-' + str(c.get_survey_date())) for c in surveys]

    def queryset(self, request, queryset):
        """method to filter survey"""
        if self.value():
            return queryset.filter(survey__id__exact=self.value())
        return None


@admin.register(Employee360QuestionResponse)
class Employee360QuestionResponseAdmin(admin.ModelAdmin):
    """Register Employee360QuestionResponse in Admin"""
    list_filter = (Employee360QuestionResponseResponseFilter,)
    list_display = ('id', 'question', 'choice')


admin.site.register(Employee360Survey)
admin.site.register(Employee360Question)
admin.site.register(Employee360Choice)

admin.site.register(CommunitySurvey)
admin.site.register(CommunityQuestion)
admin.site.register(CommunityChoice)
admin.site.register(CommunityQuestionResponse)
admin.site.register(CommunitySurveyResponse)

admin.site.register(QuestionTranslation)
admin.site.register(ChoiceTranslation)
admin.site.register(CallBack)
