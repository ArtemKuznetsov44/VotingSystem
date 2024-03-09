from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .forms import *


# Create your views here.

class RegistrationView(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'users/start_reg_auth/registration.html'

    def form_valid(self, form):
        """ Method is called when form data is valid

        :param BaseModelForm form: form with new data for new user creation
        :return HttpResponseRedirect: redirect to home page
        """

        # Create new instance of user from form data:
        user = form.save()
        # Authenticate our user:
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'users/start_reg_auth/user_login.html'
    next_page = reverse_lazy('home')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/users/profile.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')


class UsersView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/users/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return self.model.objects.exclude(pk=self.request.user.pk).order_by('last_name', 'date_joined')

    def post(self, request, *args, **kwargs):
        users_pk = [*map(int, self.request.POST.getlist('checked_users[]'))]
        if not users_pk:
            return

        get_user_model().objects.filter(pk__in=users_pk).update(is_staff=True)


# class UserProfilePreview(LoginRequiredMixin, UpdateView):
#     model = get_user_model()
#     form_class =

class AnonymousConnectionView(View):
    pass