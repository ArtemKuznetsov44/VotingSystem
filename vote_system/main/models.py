from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from . import utils
from django.db import IntegrityError

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Anonym(models.Model):
    """ Anonym model """
    unique_code = models.CharField(max_length=15, unique=True, db_index=True, blank=True)
    voting = models.ForeignKey(to='Voting', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Override save method to control unique code generation process and automize it:
        """
        while not self.unique_code:
            try:
                self.unique_code = utils.get_unique_code()
                super(Anonym, self).save(*args, **kwargs)
            except IntegrityError:
                self.unique_code = None

    def __str__(self):
        return self.unique_code


class UserParticipant(models.Model):
    """ User as voting participant model """
    voting = models.ForeignKey(to='Voting', on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voting', 'user')


class Voting(models.Model):
    """ Voting model """
    url = models.SlugField(unique=True, max_length=120)
    title = models.TextField()
    is_open = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, default='nonactive',
                              choices=(('nonactive', 'Неактивно'), ('active', 'Активно'), ('finished', 'Завершено')))
    actual_voters_count = models.PositiveSmallIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('voting-detail', kwargs={'url': self.url})

    def __str__(self):
        return f'{self.url} - {self.title}'


class Bulletin(models.Model):
    """ Bulletin model """
    voting = models.ForeignKey(to='Voting', on_delete=models.CASCADE, null=True)
    question = models.TextField()
    type = models.CharField(max_length=8, choices=(('multiple', 'Множественный выбор'), ('single', 'Одиночный ответ')),
                            default='single')
    active_status = models.BooleanField(default=False, blank=True)

    # answers = models.ManyToManyField(to='Answer', related_name='bulletin_answers')

    def __str__(self):
        return self.question


class Answer(models.Model):
    """ Answers for bulletins """
    text = models.CharField(max_length=120)
    bulletin = models.ForeignKey(to='Bulletin', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text', 'bulletin')
        index_together = ('text', 'bulletin')


class UserBulletinAnswer(models.Model):
    """ User result answer model """
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    answer = models.ForeignKey(to="Answer", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('bulletin', 'user', 'answer')


class AnonymBulletinAnswer(models.Model):
    """ Anonym result answer model """
    bulletin = models.ForeignKey(to='Bulletin', on_delete=models.CASCADE)
    anonym = models.ForeignKey(to='Anonym', on_delete=models.CASCADE)
    answer = models.ForeignKey(to='Answer', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('bulletin', 'answer')


class VotingBulletinResult(models.Model):
    pass

# class Anonym(models.Model):
#     """
#     Model for anonymous records.
#     """
#
#     voting = models.OneToOneField(to="Voting", on_delete=models.CASCADE)
#     code = models.CharField(max_length=15, unique=True, db_index=True)
#
#     def __str__(self):
#         return self.code
#
#
# class Member(models.Model):
#     """
#     Model for save members for current voting. Can save and keep data only for normal users but not stuff
#     """
#
#     user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
#     voting = models.ForeignKey(to="Voting", on_delete=models.CASCADE)
#
#     def __str__(self):
#         """
#         Method to return the title of members list in queries for example instead of id-keys
#         :return: title:str
#         """
#         return self.title
#
#     def save(self, *args, **kwargs):
#
#         if get_object_or_404(get_user_model(), pk=self.user).is_staff:
#             raise ValidationError(
#                 message=_("Администратор/сотрудник не может быть избран в качестве участника голосования"),
#                 code="invalid")
#
#         if not self.title:
#             self.title = f"Голосующие на голосовании №{self.voting}"
#         else:
#             self.title = None
#             self.title = f"Голосующие на голосовании №{self.voting}"
#
#         super().save(*args, **kwargs)
#
#     def get_absolute_url(self):
#         return reverse('members_list', kwargs={'pk': self.pk})
#
#     class Meta:
#         unique_together = ('user', 'voting')
#
#
# class Bulletin(models.Model):
#     """
#     Bulletin class - Bulletin in ONE direct question instance!
#     """
#     voting = models.ForeignKey(to='Voting', on_delete=models.CASCADE)
#     question = models.TextField()
#     type = models.CharField(max_length=8, choices=('multiple', 'single'), default='single')
#     # TODO: Maybe, here its better to use many to many field
#     answers = models.ManyToManyField(to='Answer', on_delete=models.CASCADE, related_name='bulletin_answers')
#
#     def __str__(self):
#         return self.question
#
#
# class Answer(models.Model):
#     number = models.PositiveIntegerField()
#     text = models.CharField(max_length=250)
#
#     def __str__(self):
#         return self.text
#
#
# class Voting(models.Model):
#     """
#     Voting class - Voting for db, is a binding instance.
#     Every bulletin know about it's voting.
#     Every member knows about his voting.
#     Every anonym knows about his voting.
#     """
#
#     title = models.TextField()
#     description = models.TextField(blank=True, null=True)
#     is_open = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     options = models.JSONField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#
# class AnonymResult(models.Model):
#     """
#     Model for keeping result from current anonym in voting:
#     """
#
#     bulletin = models.ForeignKey(to='Bulletin', on_delete=models.CASCADE, related_name='')
#     anonym = models.OneToOneField(to="Anonym", on_delete=models.CASCADE)
#     answers = models.ManyToManyField(to='Answer', on_delete=models.CASCADE)
#
#     class Meta:
#         """
#         Special Meta class for give some extra options to the model:
#         * unique_together - options to make voting and anonym as unique pair
#         """
#         unique_together = ('bulletin', 'anonym')
