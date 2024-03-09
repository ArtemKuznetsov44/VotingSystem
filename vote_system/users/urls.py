from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # URLs for Anonymous:
    path('anonym-connection/', AnonymousConnectionView.as_view(), name='anonym_connection'),


    # URLs for Users:
    # To see all existing Users in system as list:
    path('all-users/', UsersView.as_view(), name='all-users'),
    # To update or have a look the user profile info:
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('user-preview/<slug:slug>', OneUserPrevie)
    # To sign out from user account:
    path('sign-out/', LogoutView.as_view(), name='sign_out'),
    # For registration (new user creation):
    path('registration/', RegistrationView.as_view(), name='registration'),
    # For authentication our user in system (to sign in system):
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    # path('user-profile-preview/', UserProfilePreview.as_view(), name='user-profile-preview')
]