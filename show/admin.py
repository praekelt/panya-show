from django import forms
from django.contrib import admin

from panya.admin import ModelBaseAdmin
from preferences import preferences
from show.models import Appearance, Credit, CreditOption, RadioShow, ShowContributor, ShowPreferences

class CreditOptionInline(admin.TabularInline):
    model = CreditOption

class ShowPreferencesAdmin(admin.ModelAdmin):
    inlines = [
        CreditOptionInline,
    ]

class CreditInlineAdminForm(forms.ModelForm):
    role = forms.ChoiceField(
        label='Role', 
    )
    class Meta:
        model = Credit

    def __init__(self, *args, **kwargs):
        """
        Set role choices to credit options
        """
        role_choices = []
        credit_options = preferences.ShowPreferences.creditoption_set.all()
        for credit_option in credit_options:
            role_choices.append((credit_option.role_priority, credit_option.role_name))

        self.declared_fields['role'].choices = [('', '---------'),] + role_choices
        super(CreditInlineAdminForm, self).__init__(*args, **kwargs)

class CreditInline(admin.TabularInline):
    form = CreditInlineAdminForm
    model = Credit

class RadioShowAdmin(ModelBaseAdmin):
    inlines = (
        CreditInline, 
    )

class AppearanceInline(admin.TabularInline):
    model = Appearance

class ShowContributorAdmin(ModelBaseAdmin):
    inlines = (
        AppearanceInline, 
    )
    
admin.site.register(RadioShow, RadioShowAdmin)
admin.site.register(ShowContributor, ShowContributorAdmin)
admin.site.register(ShowPreferences, ShowPreferencesAdmin)
