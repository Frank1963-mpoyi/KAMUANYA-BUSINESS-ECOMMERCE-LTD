from django                                                     import forms
from django.db.models                                           import Q
from django.core.validators                                     import RegexValidator

from crispy_forms.helper                                        import FormHelper



USERNAME_REGEX     = '^[a-zA-Z0-9.+-]*$'
PHONE_NUMBER_REGEX = '^[ 0-9]+$'


class GetInTouchForm(forms.Form):

    fullname            = forms.CharField(label='Full name',    widget=forms.TextInput(attrs={"title" : "Full name", "class":"form-control", "placeholder":"Full name ... "}),              required=False)
    email1              = forms.CharField(label='email1',       widget=forms.EmailInput(attrs={"title": "email", "class":"form-control", "placeholder":"Email address.."}),                 required=False)
    subject             = forms.CharField(label='subject',      widget=forms.TextInput(attrs={"title" : "subject", "class":"form-control", "placeholder":"Subject"}),                       required=False)
    message             = forms.CharField(label='message',      widget=forms.Textarea(attrs={"title": "message", "class": "form-control", "row": "3", "placeholder": "Enter message.."}),   required=False)

    def clean(self):
        cleaned_data    = super(GetInTouchForm, self).clean()

        fullname        = cleaned_data.get('fullname')
        subject         = cleaned_data.get('subject')
        email1          = cleaned_data.get('email1')

        if not fullname:
            self.add_error('fullname', "Please put  your fullname. ")

        if not email1:
            self.add_error('email1', "Please put your email address. ")

        if not subject:
            self.add_error('subject', "Please put your subject. ")

        return cleaned_data