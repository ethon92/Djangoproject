from django import forms
from django.forms import PasswordInput

class login_form(forms.Form):
    username = forms.CharField(required=True)
    passqord = forms.CharField(required=True,widget=PasswordInput)