from django import forms
from django.contrib import admin

from content.admin import ModelBaseAdmin
from options import options
from show.models import Credit, CreditOption, RadioShow, ShowContributor, ShowOptions

class CreditOptionInline(admin.TabularInline):
    model = CreditOption

class ShowOptionsAdmin(admin.ModelAdmin):
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
        credit_options = options.ShowOptions.creditoption_set.all()
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
    
admin.site.register(RadioShow, RadioShowAdmin)
admin.site.register(ShowContributor, ModelBaseAdmin)
admin.site.register(ShowOptions, ShowOptionsAdmin)
