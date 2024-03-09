from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Anonym(models.Model):
    """
    Model for anonymous records.
    """

    voting = models.OneToOneField(to="Voting", on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True, db_index=True)

    def __str__(self):
        return self.code


class MembersList(models.Model):
    """
    Model for save members for current voting. Can save and keep data only for normal users but not stuff
    """

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(to="Voting", on_delete=models.CASCADE)

    def __str__(self):
        """
        Method to return the title of members list in queries for example instead of id-keys
        :return: title:str
        """
        return self.title

    def save(self, *args, **kwargs):

        if get_object_or_404(get_user_model(), pk=self.user).is_staff:
            raise ValidationError(
                message=_("Администратор/сотрудник не может быть избран в качестве участника голосования"),
                code="invalid")

        if not self.title:
            self.title = f"Голосующие на голосовании №{self.voting}"
        else:
            self.title = None
            self.title = f"Голосующие на голосовании №{self.voting}"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('members_list', kwargs={'pk': self.pk})


class Bulletin(models.Model):
    """
    Model for keeping info about bulletins
    """

    title = models.CharField(max_length=200, blank=False, null=False)

    # Bulletin related key-option to get voting with it (bulletin.voting_set.all() - as example):
    voting = models.ForeignKey(to="Voting", on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Method to configure the object string representation as it's title
        :return:
        """

        return self.title

    def get_absolute_url(self):
        return reverse('bulletin', kwargs={'pk': self.pk})


class Voting(models.Model):
    """
    Model for keeping info about voting processes
    """

    # Main voting title
    title = models.CharField(max_length=200, blank=False, null=False)

    # Field for adding some more info about current voting process. May be used, may not
    special_info = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    options = models.OneToOneField(to="VotingOption", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Method to configure the object string representation as it's title.
        :return:
        """

        return self.title


class VotingOption(models.Model):
    """
    Simple model just for keeping different options for one voting process
    """

    options = models.JSONField()


class Question(models.Model):
    """
    Model of question. Is has information about question type and bulletin.
    """
    question = models.TextField(null=False, blank=False)
    type = models.ForeignKey(to="QuestionType", on_delete=models.PROTECT)
    bulletin = models.ForeignKey(to="Bulletin", on_delete=models.CASCADE, null=True, blank=True)
    answers = models.JSONField(blank=False, null=False)

    def __str__(self):
        # result_str =  f'''{self.question}:\n'''
        # for answer in enumerate(self.answers):
        #     result_str += f'''{answer}'
            
        return self.question


class QuestionType(models.Model):
    """
    Model for keeping question types: multiple choice or one choice for now as example.
    """

    type_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.type_name


class UserResult(models.Model):
    """
    Model for keeping result from current user in voting
    """

    voting = models.ForeignKey(to="Voting", on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    answers = models.JSONField()

    class Meta:
        """
        Special Meta class for give some extra options to the model:

        * unique_together - option to make voting and user as unique pair
        """

        # In our DB we could not have two records with the same field values in voting and user
        # - ONE USER only with ONE RESULT FOR ONE VOTING:
        unique_together = ('voting', 'user')


class AnonymResult(models.Model):
    """
    Model for keeping result from current anonym in voting:
    """

    voting = models.ForeignKey(to="Voting", on_delete=models.CASCADE)
    anonym = models.OneToOneField(to="Anonym", on_delete=models.CASCADE)
    answers = models.JSONField()

    class Meta:
        """
        Special Meta class for give some extra options to the model:
        * unique_together - options to make voting and anonym as unique pair
        """
        unique_together = ('voting', 'anonym')
