from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    fullname = forms.CharField(label='', widget=forms.TextInput(attrs={"title": "Full name ", "class":"form-control", "id":"fullname"}),required=False)
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={"title": "E-mail Adress", "class":"form-control", "id":"emailAddress"}),required=False)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"title": "password", "class":"form-control",  "id":"myInput"}),required=False)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"title": "Confirm Password ", "class":"form-control", "id":"myInput"}),required=False)

    class Meta:
        model = User
        fields = ['fullname', 'email',]

    def clean(self):
        fullname = self.cleaned_data.get('fullname')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if not fullname:
            self.add_error('fullname', "Please put your Full name")

        if not email:
            self.add_error('email', "Please put your email address")

        if not password:
            self.add_error('password', "Please put your password.")

        if password and password1 and password != password1:
            self.add_error('password1', "your password is not matched.")

        user = User.objects \
            .filter(
                Q(username__iexact = email) |
                Q(email__iexact = email)
            ) \
            .exclude(
                Q(bool_deleted = True)
            )

        if user:
            raise forms.ValidationError("This account has been used please take another one.")
        
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={"title" : "email adress", "class":"form-control", "id":"emailAddress" }), required=False)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={"title" : "password","class":"form-control",  "id":"myInput" }), required=False)

    def clean(self, *args, **kwargs):
        email    = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        username_or_email_final = User.objects \
            .filter(
                Q(username__iexact = email) |
                Q(email__iexact = email)
            ) \
            .exclude(
                Q(bool_deleted  = True)
            ) \
            .distinct()

        if not email:
            self.add_error('email', "Please put your email address")

        if not password:
            self.add_error('password', "Please confirm your password ")

        if not username_or_email_final.exists() and username_or_email_final != 1:
            raise forms.ValidationError("You don't have an account with us you must register ")

        user_obj = username_or_email_final.first()

        if not user_obj.check_password(password):
            raise forms.ValidationError("your informations are not correct please try again !")

        self.cleaned_data['user_obj'] = user_obj

        return self.cleaned_data