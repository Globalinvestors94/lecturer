from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile,Lecturer_View,Assignment_Answers,Quiz_Answers, Scratch_Pin


class PYT(forms.ModelForm):
    class Meta:
        model = Lecturer_View
        fields = ['programme', 'year', 'task', 'upload', 'number_of_student']


class Scratch_Pin_Form(forms.ModelForm):
    class Meta:
        model = Scratch_Pin
        fields = ['user', 'programme', 'year', 'task', 'student_reg','number']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']


class QP(forms.ModelForm):
    class Meta:
        model = Lecturer_View
        fields = ['programme', 'year','task']


class PinFilter(forms.ModelForm):
    class Meta:
        model = Lecturer_View
        fields = ['programme', 'year']

class MoreSignUpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =["pics","phone","degree","gender"]


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)



class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class AA(forms.ModelForm):
    class Meta:
        model = Assignment_Answers
        fields = ['name', 'reg_number', 'ass_upload'] 


class AS(forms.ModelForm):
    class Meta:
        model = Assignment_Answers
        fields = ['score']

class QuizAA(forms.ModelForm):
    class Meta:
        model = Quiz_Answers
        fields = ['name', 'reg_number', 'quiz_upload'] 


class QS(forms.ModelForm):
    class Meta:
        model = Quiz_Answers
        fields = ['score']



class PinForm(forms.Form):
    pin = forms.IntegerField(label='Pin Number')
    reg_number = forms.IntegerField(label='Reg Number')


class EmailForm(forms.Form):
    email = forms.EmailField()