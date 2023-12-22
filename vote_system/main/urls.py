from django.urls import path
from .views import *

urlpatterns = [
    path('', StartPage.as_view(), name='start'),
    path('home/', HomePage.as_view(), name='home'),
    path('sign-in/', UserSingInPage.as_view(), name='sign_in'), 
    path('anonym-connection/', AnonymConnectionPage.as_view(), name='anonym_connection'),
    path('sign-out/', UserSingOutPage.as_view(), name='sign_out'), 
    path('registration/', UserRegistrationPage.as_view(), name='registration'),
    path('voting/', VotingPage.as_view(), name='voting_all'),
    path('users/', UsersPage.as_view(), name='users'),
    path('bulletins/', BulletinsPage.as_view(), name='bulletins'),
    path('results/', ResultsPage.as_view(), name='results')
]