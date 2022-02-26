from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passcode
from django import forms
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField


class MyUserCreation(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password = self.cleaned_data.get("password2")
        if password1 and password and password1 != password:
            raise forms.ValidationError( "The two password fields didn't match. you have")
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError( "the email filed is empty")
        elif len(User.objects.filter(email=email)) > 0:
            raise forms.ValidationError("the email is already used please sign up with another email")
        return email


