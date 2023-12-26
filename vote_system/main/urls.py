from django.urls import path
from .views import *

urlpatterns = [
    path('', StartPage.as_view(), name='start'),
    path('home/', HomePage.as_view(), name='home'),

    # URLs for Anonymous:
    path('anonym-connection/', AnonymConnectionPage.as_view(), name='anonym_connection'),


    # URLs for Voting:
    # To see all existing Voting in system as list:
    path('voting/', VotingPage.as_view(), name='voting_all'),
    path('voting/creation/', VotingCreatePage.as_view(), name='voting_create'),
    path('voting/detail_id_<int:pk>/', VotingShowAndUpdatePage.as_view(), name='voting'),


    # URLs for Users:
    # To see all existing Users in system as list:
    path('users/', UsersPage.as_view(), name='users'),
    # To update or have a look the user profile info:
    path('profile/<slug:slug>', ProfilePage.as_view(), name='profile'),
    # To sign out from user account:
    path('sign-out/', UserSingOutPage.as_view(), name='sign_out'),
    # For registration (new user creation):
    path('registration/', UserRegistrationPage.as_view(), name='registration'),
    # For authentication our user in system (to sign in system):
    path('sign-in/', UserSingInPage.as_view(), name='sign_in'),


    # URLs for Bulletins:
    # To see all existing bulletins:
    path('bulletins/', BulletinsListPage.as_view(), name='bulletins_all'),
    # Look and update bulletin:
    path('bulletins/detail_for=<int:pk>/', BulletinShowAndUpdatePage.as_view(), name='bulletin'),
    # For bulletin creation:
    path('bulletins/create/', BulletinCreatePage.as_view(), name='bulletin_create'),


    # URLs for results:
    path('results/', ResultsPage.as_view(), name='results'),


    # URLs for ajax handlers views:
    path('add_question_ajax/', AddQuestionAjax.as_view(), name='add_question_ajax')
]