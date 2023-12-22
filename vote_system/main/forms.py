from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.forms.widgets import *
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label='Логин',
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=30,
        label='Фамилия', required=True,
        widget=TextInput(
            attrs={'class': 'form-control'})
    )

    father_name = forms.CharField(
        max_length=30,
        label='Отчество',
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        max_length=16,
        label='Телефон',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+7-9XX-XX-XX'}
        )
    )
    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=True,
        widget=DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'format': '%d %b %Y',
                   'min': '1920-01-01', 'max': date.today().strftime('%Y-%m-%d')}
        )
    )

    password1 = forms.CharField(
        max_length=18,
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    password2 = forms.CharField(
        max_length=18,
        label='Повторите пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'father_name', 'username',
                  'phone', 'date_of_birth', 'password1', 'password2']


class UserSignInForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        label='Логин',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password = forms.CharField(
        max_length=18,
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class AnonymCreationForm(forms.ModelForm):
    model = Anonym
