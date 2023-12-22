from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import * 
from .forms import *


menu = [
    {'id': 1, 'name': 'Голосования', 'url_name': 'voting_all'},
    {'id': 2, 'name': 'Бюллетени', 'url_name': 'bulletins'},
    {'id': 3, 'name': 'Результаты', 'url_name': 'results'},
    {'id': 4, 'name': 'Пользователи', 'url_name': 'users'},
]

# Create your views here.

class StartPage(View):

    def get(self, request):
        if self.request.user and self.request.user.is_authenticated:
            return redirect('home')
        
        return render(self.request, 'main/start_page.html')


class HomePage(View):
    """
    Class to display home|start page
    """

    def get(self, request):
        if not self.request.user or not self.request.user.is_authenticated:
            return redirect('start')

        return render(request=self.request, template_name='main/home.html', context={'menu': menu})


class UserRegistrationPage(CreateView): 
    """ View with form for create new user

    :param CreateView: Default CreateView class from django
    """
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'main/registration.html'
    
    
    def form_valid(self, form):
        """ Method is called when form data is valid

        :param BaseModelForm form: form with new data for new user creation
        :return HttpResponseRedirect: redirect to home page
        """
        
        # Create new instance of user from form data:
        user = form.save()
        # Authentificate our user:
        login(self.request, user)
        return redirect('home')
    
    
    # def get_success_url(self): 
    #     return reverse_lazy('home')
    

class UserSingInPage(LoginView):
    """ View to dispaly login form for user and for admin. 

    :param LoginView: Default LoginView class from django
    """
    form_class = UserSignInForm
    template_name = 'main/user_login.html'
    
    def get_success_url(self): 
        return reverse_lazy('home')
    
        


class UserSingOutPage(LogoutView):
    """ View just to logout from user/admin account

    :param LogoutView: Default LogoutView from django
    """
    
    def get_success_url(self): 
        return reverse_lazy('start')


class AnonymConnectionPage(View):
    
    def get(self, request): 
        """_summary_

        :param HttpRequest request: I don't now for what... View already has self.request
        """
        pass
    pass

class VotingPage(ListView):
    pass

class BulletinsPage(ListView):
    pass

class UsersPage(ListView):
    pass

class ResultsPage(ListView):
    pass