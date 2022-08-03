from dataclasses import field
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):

    phone_number = forms.CharField(max_length=10, 
                        widget=forms.TextInput(attrs={
                            'class': 'form-control', 'placeholder': 'Номер телефона'}))
    
    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={
                               'class': 'form-control', 'placeholder': 'Пароль'})) 


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'group': forms.HiddenInput()
        }


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль', 'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control'})

    class Meta:
        model = Teacher
        fields = (
            'email',
            'phone_number',
            'name',
            'gender',
            'group',
            'avatar',
            'password1',
            'password2',
        )

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Почта', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'form-control'}),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Номер телефона', 'class': 'form-control'}),
            'gender': forms.RadioSelect(),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'iamge/*'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Заголовок', 
                    'class': 'form-control'}),
            'password2': forms.PasswordInput(
                attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control'}),
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('title',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        