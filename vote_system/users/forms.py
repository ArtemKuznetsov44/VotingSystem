from datetime import date
from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, EmailValidator, MinLengthValidator, MaxValueValidator

from .models import *
from django.forms.widgets import *
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, label='Логин',
        widget=TextInput(
            attrs={'class': 'form-control'}
        )
    )

    first_name = forms.CharField(
        max_length=30, label='Имя',
        widget=TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        max_length=30, label='Фамилия',
        widget=TextInput(
            attrs={'class': 'form-control'}
        )
    )

    father_name = forms.CharField(
        max_length=30, label='Отчество',
        widget=TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        validators=[EmailValidator(message='Введенный E-mail не валидный')]

    )

    phone = forms.CharField(
        max_length=16, label='Телефон',
        min_length=16,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+7-9XX-XX-XX'}
        )
    )

    date_of_birth = forms.DateField(
        label='Дата рождения',
        widget=DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'format': '%d %b %Y',
                   'min': '1920-01-01', 'max': date.today().strftime('%Y-%m-%d')}
        )
    )

    password1 = forms.CharField(
        label='Пароль',
        max_length=18,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}
        )
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        max_length=18,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['last_name', 'first_name', 'father_name', 'username', 'email',
                  'phone', 'date_of_birth', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(message="Указанный E-mail уже существует...", code='invalid')
        return email


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30, label='Логин | E-mail',
        min_length=5,
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        )
    )

    password = forms.CharField(
        max_length=18, label='Пароль',
        min_length=4,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password'}
        )
    )


class UserUpdateForm(forms.ModelForm):
    profile_img = forms.ImageField(
        label="Фотография", required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )

    first_name = forms.CharField(
        max_length=30, label='Имя',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        max_length=30, label='Фамилия',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    father_name = forms.CharField(
        max_length=30,
        label='Отчество',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    username = forms.CharField(
        max_length=30,
        label='Логин',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+7-9XX-XX-XX'}
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        validators=[EmailValidator(message='Введенный E-mail не валидный')]

    )

    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=True,
        widget=DateInput(
            attrs={'type': 'date', 'class': 'form-control', 'format': '%d %b %Y',
                   'min': '1920-01-01', 'max': date.today().strftime('%Y-%m-%d')}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['profile_img', 'last_name', 'first_name', 'father_name', 'username', 'phone', 'email',
                  'date_of_birth']


# class UserProfilePreviewForm(forms.ModelForm):
#
#     first_name = forms.CharField(
#         max_length=30, label='Имя',
#         disabled=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}
#         )
#     )
#
#     last_name = forms.CharField(
#         max_length=30, label='Фамилия',
#         disabled=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}
#         )
#     )
#
#     father_name = forms.CharField(
#         max_length=30,
#         label='Отчество',
#         disabled=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}
#         )
#     )
#
#     phone = forms.CharField(
#         max_length=30,
#         required=True,
#         disabled=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': '+7-9XX-XX-XX'}
#         )
#     )
#
#     email = forms.EmailField(
#         required=False,
#         disabled=True,
#         widget=forms.EmailInput(
#             attrs={'class': 'form-control'}
#         ),
#         validators=[EmailValidator(message='Введенный E-mail не валидный')]
#
#     )
#
#     date_of_birth = forms.DateField(
#         label='Дата рождения',
#         required=True,
#         disabled=True,
#         widget=DateInput(
#             attrs={'type': 'date', 'class': 'form-control', 'format': '%d %b %Y',
#                    'min': '1920-01-01', 'max': date.today().strftime('%Y-%m-%d')}
#         )
#
#     )
#
#     class Meta:
#         model = get_user_model()
#         fields = ['last_name', 'first_name', 'father_name', 'phone', 'email',
#                   'date_of_birth', 'is_staff']
#