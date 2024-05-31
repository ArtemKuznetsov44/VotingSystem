from datetime import date
from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, EmailValidator, MinLengthValidator, MaxValueValidator, \
    MaxLengthValidator

from .models import *
from django.forms.widgets import *
from django.core.exceptions import ValidationError
from main.models import Anonym


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            MinLengthValidator(limit_value=8, message='Логин слишком короткий'),
            MaxLengthValidator(limit_value=30, message='Логин слишком длинный')
        ]
    )

    first_name = forms.CharField(
        label='Имя',
        widget=TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            MinLengthValidator(limit_value=2, message='Имя слишком короткое'),
            MaxLengthValidator(limit_value=50, message='Имя слишком длинное')
        ]

    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            MinLengthValidator(limit_value=2, message='Фамилия слишком короткая'),
            MaxLengthValidator(limit_value=50, message='Фамилия слишком длинная'),
        ]
    )

    father_name = forms.CharField(
        label='Отчество',
        widget=TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            MinLengthValidator(limit_value=2, message='Отчество слишком короткое'),
            MaxLengthValidator(limit_value=30, message='Отчество слишком длинное')
        ]
    )

    email = forms.EmailField(
        label='E-mail',
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            EmailValidator(message='Введенный E-mail не валидный'),
            MinLengthValidator(limit_value=5, message='E-mail слишком короткий')
        ]
    )

    phone = forms.CharField(
        label='Телефон',
        max_length=16,
        min_length=16,
        validators=[
            MinLengthValidator(limit_value=16, message='Не верный формат телефона'),
            MaxLengthValidator(limit_value=16, message='Не верный формат телефона')
        ]
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
        ),
        validators=[
            MinLengthValidator(limit_value=8, message='Пароль должен состоять минимум из 8 символов'),
            MaxLengthValidator(limit_value=18, message='Длина пароле не должна быть более 18 символов')
        ]
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


class AnonymConnectionForm(forms.Form):
    unique_code = forms.CharField(
        label='Ваш код',
        widget=forms.TextInput(
            attrs={'class': 'form-control'},
        ),
        validators=[MaxLengthValidator(limit_value=15, message='Введенный код слишком короткий')]

    )
    # class Meta:
    #     model = Anonym
    #     fields = ('unique_code',)
    #     labels = {
    #         'unique_code': 'Ваш код'
    #     }
    #     widgets = {
    #         'unique_code': forms.TextInput(
    #             attrs={'class': 'form-control'}
    #         )
    #     }


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
        label='Телефон',
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+7-9XX-XX-XX'}
        )
    )

    email = forms.EmailField(
        label='E-mail',
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
