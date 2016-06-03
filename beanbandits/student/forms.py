from django import forms
from registration.forms import RegistrationForm
from .choices import *

class ExtendedForm(RegistrationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(),
        label="first_name")
    proficiency = forms.ChoiceField(
        choices=PROFICIENCY_CHOICES,
        label="proficiency",
        widget=forms.Select(),
        required=True,
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="gender",
        widget=forms.Select(),
        required=True,
    )
    age = forms.IntegerField(label="age")
