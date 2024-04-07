from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, EmailValidator, MinLengthValidator, MaxValueValidator

from .models import *
from django.forms.widgets import *
from django.core.exceptions import ValidationError


class VotingCreationForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    description = forms.CharField(
        label='Доп. описание',
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '5'}
        )
    )

    is_open = forms.BooleanField(
        label='Открытое голосование',
        initial=True,
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'id': 'is-open-switch'}
        )
    )

    users = forms.ModelMultipleChoiceField(
        label='Добавление участников',
        queryset=get_user_model().get_not_staff_users(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    anonyms = forms.IntegerField(
        label='Добавление анонимных участников',
        required=False,
        initial=2,
        widget=forms.NumberInput(attrs={'class': 'form-range', 'type':'range', 'min': 2, 'max': 100}),
        validators=[MinValueValidator(2, 'В голосовании может быть не менее двух участников'),
                    MaxValueValidator(100)]
    )

    bulletins = forms.ModelMultipleChoiceField(
        label='Бюллетени',
        queryset=Bulletin.objects.filter(voting__isnull=True),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Voting
        fields = ('title', 'is_open', 'description')


class AddBulletinForm(forms.ModelForm):
    question = forms.CharField(
        label='Вопрос',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        validators=[MinLengthValidator(limit_value=10, message='Неправдоподобно короткий вопрос')]
    )

    type = forms.ChoiceField(
        choices=(('single', 'Одиночный ответ'), ('multiple', 'Множественный выбор')),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    class Meta:
        model = Bulletin
        fields = ('question', 'type')
        # labels = {
        #     'question': 'Вопрос',
        #     'type': 'Тип'
        # }
        # widgets = {
        #     'question': forms.TextInput(attrs={'class': 'form-control'}),
        #     'type': forms.Select(attrs={'class': 'form-select'})
        # }


class AnonymCreationForm(forms.Form):
    count = forms.IntegerField(
        label='Создать',
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'from-control'}
        ),
        validators=[MinValueValidator(1, message='Нельзя создать меньше одного анонима'),
                    MaxValueValidator(100, message='Укажите число меньше 100')]
    )

# class QuestionCreateForm(forms.ModelForm):
#     question = forms.CharField(
#         label='Вопрос',
#         required=True,
#         widget=forms.Textarea(
#             attrs={'class': 'form-control', 'rows': '2', 'cols': '40'}
#         ),
#         validators=[MinLengthValidator(limit_value=20, message='Слишком короткий вопрос')]
#     )
#
#     type = forms.ModelChoiceField(
#         label='Тип вопроса',
#         queryset=QuestionType.objects.all(),
#         required=True,
#         empty_label='Не выбрано',
#         widget=forms.Select(
#             attrs={'class': 'form-control'}
#         ),
#         validators=[MinValueValidator(limit_value=1, message='Укажите тип вопроса'),
#                     MaxValueValidator(limit_value=3, message="Укажите тип вопроса")]
#     )
#
#     class Meta:
#         model = Question
#         fields = ['type', 'question']


# class BulletinForm(forms.ModelForm):
#     title = forms.CharField(
#         label='Заголовок',
#         required=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}
#         ),
#         validators=[MinLengthValidator(limit_value=20, message='Слишком короткий заголовок бюллетени')]
#     )
#
#     voting_id = forms.ModelChoiceField(
#         label='К голосованию',
#         queryset=Voting.objects.all(),
#         required=False,
#         empty_label="Без привязки",
#         widget=forms.Select(
#             attrs={'class': 'form-select'}
#         )
#     )
#
#     class Meta:
#         model = Bulletin
#         fields = ['title', 'voting_id']
#
#
# class VotingCreationForm(forms.ModelForm):
#     title = forms.CharField(
#         label='Название',
#         required=True,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}
#         )
#     )
#
#     special_info = forms.CharField(
#         label='Дополнительное описание',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'class': 'form-control'}IntegerField
#         )
#     )
#
#     is_open = forms.BooleanField(
#         label='Открытое голосование',
#         widget=forms.CheckboxInput(),
#         initial=True,
#         required=False
#     )
#
#     bulletins = forms.ModelMultipleChoiceField(
#         label='Бюллетени',
#         queryset=Bulletin.objects.filter(voting__isnull=True),
#         widget=forms.CheckboxSelectMultiple(),
#     )
#
#     users = forms.ModelMultipleChoiceField(
#         label='Пользователи',
#         queryset=get_user_model().objects.filter(is_staff=False),
#         widget=forms.CheckboxSelectMultiple(),
#         required=False,
#         # validators=[MinValueValidator(2, message="В голосовании должно быть минимум два участника")]
#     )
#
#     anonymous = forms.IntegerField(
#         label='Добавить анонимных участников',
#         widget=forms.NumberInput(),
#         initial=1,
#         validators=[MinValueValidator(1, message='В голосовании должно быть более 2-х участников'),
#                     MaxValueValidator(100, message=f'В голосование можно добавить не более 100 участников'),],
#         required=False
#     )
#
#     options = forms.JSONField(
#         label='Опции в формате JSON',
#         widget=forms.Textarea(attrs={'rows': '5', 'cols': '60', 'class': 'form-control'}),
#         required=False
#     )
#
#     class Meta:
#         model = Voting
#         fields = ['title', 'special_info', 'is_open']
