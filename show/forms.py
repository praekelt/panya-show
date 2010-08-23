from django import forms
from django.conf import settings
from django.core.mail import mail_admins, send_mail
        
class ShowContributorContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class':'required'}),
        error_messages={'required': 'Please enter your first name.'}
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class':'required'}),
        error_messages={'required': 'Please enter your surname.'}
    )
    email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class':'required'}),
        error_messages={'required': 'Please enter your email address.'}
    )
    message = forms.CharField(
        max_length=1500,
        widget=forms.Textarea(attrs={'class':'required'}),
        error_messages={'required': 'Please enter your message.'}
    )
    honeypot = forms.CharField(
        max_length=50,
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super(ShowContributorContactForm, self).__init__(*args, **kwargs)
        self.contributor = kwargs.get('contributor', None)
        
    def is_valid(self, *args, **kwargs):
        is_valid = super(ShowContributorContactForm, self).is_valid(*args, **kwargs)
        if is_valid:
            if not self.cleaned_data['honeypot']:
                return True
    
    def handle_valid(self, contributor, *args, **kwargs):
        if not contributor.owner.email:
            mail_admins("Contact Error", "Message could not be sent to %s. No email address specified." % contributor.owner.email, fail_silently=True)
            return None
        else:
            subject = "Email from website."
            message = "%s sent you a message from the website:\r\n\r\n" % self.cleaned_data.get('first_name')
            for key, val in self.cleaned_data.iteritems():
                 if key != "honeypot":
                    message += "%s: %s\r\n" % (key.title().replace("_", " "), val)
            from_email = self.cleaned_data.get('email')
            to_email = [contributor.owner.email]
            
            send_mail(subject, message, from_email, to_email)
            
            return None
