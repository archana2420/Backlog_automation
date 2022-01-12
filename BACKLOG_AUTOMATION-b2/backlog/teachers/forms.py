from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

search_types= (
    ("dummy", "Select "),
    ("subject", "Subject"),
    ("subject_code", "Subject Code"),
    ("exam_type", "Exam_type"),
    ("department", "Department"),
    ("sem", "Semester"),
)

class staff_form(forms.Form):
    email = forms.EmailField(max_length=32, label="Email")
    password = forms.CharField(widget=forms.PasswordInput , label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")

class staff_loginForm(forms.Form):
    email = forms.EmailField(max_length=32, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']



class search_form(forms.Form):
    content=forms.CharField(max_length=50,label="Search:")
    search_choice=forms.ChoiceField(choices=search_types, label='Search type:')


