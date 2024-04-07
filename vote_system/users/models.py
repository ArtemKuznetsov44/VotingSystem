from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Extra methods from myself to help models:
def user_profile_img_path(instance, filename) -> str:
    """
    Method to configure the url or path for User profile img in default and base MEDIA_ROOT directory
    :param instance: current User
    :param filename: string name of file from form
    :return: string path in media directory
    """
    return 'uploads/{username}/profile-img/{filename}'.format(username=instance.username, filename=filename)


# Create your models here.
class User(AbstractUser):
    """
    User model which is based on AbstractUser

    Default fields from AbstractUser:
    * username
    * first_name
    * last_name
    * email
    * is_stuff(property)
    * data_joined
    """

    slug = models.SlugField(db_index=True)
    father_name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=16, null=True, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    profile_img = models.ImageField(upload_to=user_profile_img_path, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True, db_index=True)

    @staticmethod
    def get_not_staff_users():
        return User.objects.filter(is_staff=False)

    # Extend the base save method - it is called before saving object as record into the database:
    def save(self, *args, **kwargs):
        """
        Overwritten method which is called before saving current User record into the database
        It is used for slugify username
        :param args:
        :param kwargs:
        :return: None
        """

        if not self.slug:
            self.slug = slugify(self.username)
        else:
            self.slug = None
            self.slug = slugify(self.username)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Method to get absolute url address for current instance.
        Can be useful for making path to the profile user page by his or her slug
        :return:
        """

        return reverse("profile", kwargs={"slug": self.slug})

    def __str__(self):
        return ' '.join([self.first_name, self.father_name, self.last_name])
