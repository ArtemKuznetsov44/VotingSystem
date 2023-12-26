from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, EmailValidator

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


class UserUpdateForm(forms.ModelForm):
    profile_img = forms.ImageField(
        label="Фотография",
        required=False,
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )

    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        max_length=30,
        label='Фамилия',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    father_name = forms.CharField(
        max_length=30,
        label='Отчество',
        required=True,
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
        model = User
        fields = ['profile_img', 'first_name', 'last_name', 'father_name', 'username', 'phone', 'email',
                  'date_of_birth']


class AnonymCreationForm(forms.ModelForm):
    model = Anonym
    pass


class QuestionCreateForm(forms.ModelForm):
    question = forms.CharField(
        label='Вопрос',
        required=True,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '2', 'cols': '40'}
        )
    )

    type = forms.ModelChoiceField(
        label='Тип вопроса',
        queryset=QuestionType.objects.all(),
        required=True,
        empty_label='Не выбрано',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Question
        fields = ['type', 'question']


class BulletinCreationForm(forms.ModelForm):

    title = forms.CharField(
        label="Заголовок",
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    voting_id = forms.ModelChoiceField(
        label="К голосованию",
        queryset=Voting.objects.all(),
        required=False,
        empty_label="Без привязки",
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )

    )

    questions = forms.ModelMultipleChoiceField(
        label='Вопросы',
        queryset=Question.objects.filter(bulletin__isnull=True),
        widget=forms.CheckboxSelectMultiple(),

    )

    class Meta:
        model = Bulletin
        fields = ['title', 'voting_id']

    def __init__(self, *args, **kwargs):
        super(BulletinCreationForm, self).__init__(*args, **kwargs)
        self.fields['questions'].initital = Question.objects.filter(bulletin__isnull=True)


class BulletinUpdateForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = Bulletin
    #     fields = ['title', 'voting_id']
    #
    # def __init__(self, *args, **kwargs):
    #     super(BulletinUpdateForm, self).__init__(*args, **kwargs)




class VotingCreationForm(forms.ModelForm):

    title = forms.CharField(
        label='Название',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    special_info = forms.CharField(
        label='Дополнительное описание',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    is_open = forms.BooleanField(
        label='Открытое голосование',
        widget=forms.CheckboxInput(),
        initial=True
    )

    users = forms.ModelMultipleChoiceField(
        label='Пользователи',
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple(),
        # validators=[MinValueValidator(2, message="В голосовании должно быть минимум два участника")]
    )

    options = forms.JSONField(
        label='Опции в формате JSON',
        widget=forms.Textarea(attrs={'rows': '5', 'cols': '60', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Voting
        fields = ['title', 'special_info', 'is_open']