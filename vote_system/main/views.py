import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView, CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


# Create your views here.

class StartPage(View):
    """
    Class to display start page
    """

    def get(self, request):
        if self.request.user and self.request.user.is_authenticated:
            return redirect('home')

        return render(self.request, 'main/start_page.html')


class HomePage(DataMixin, LoginRequiredMixin, View):
    """
    Class to display home|start page
    """
    login_url = reverse_lazy('sign_in')

    def get(self, request):
        context = self.get_user_context(selected=0)
        return render(request=self.request, template_name='main/home.html', context=context)


class UserRegistrationPage(CreateView):
    """
    Class to display registration page
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
        # Authenticate our user:
        login(self.request, user)
        return redirect('home')


class UserSingInPage(LoginView):
    """
    Class to display user|sing in page
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


class ProfilePage(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = 'main/profile.html'
    form_class = UserUpdateForm
    model = User

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug', self.request.user.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context(), 'user': self.object}


class AnonymConnectionPage(View):

    def get(self, request):
        """_summary_

        :param HttpRequest request: I don't now for what... View already has self.request
        """
        pass

    pass


class VotingPage(DataMixin, ListView):
    model = Voting
    template_name = 'main/voting.html'
    context_object_name = 'voting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}


class VotingCreatePage(DataMixin, CreateView):
    model = Voting
    template_name = 'main/voting_creation.html'
    form_class = VotingCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        new_voting = form.save()

        for user in cleaned_data['users']:
            MembersList.objects.create(user=user, voting=new_voting).save()

        return redirect('voting')


class VotingShowAndUpdatePage(DataMixin, UpdateView):
    model = Voting
    template_name = 'main/voting_update.html'
    form_class = VotingCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}


class BulletinsListPage(DataMixin, ListView):
    model = Bulletin
    template_name = 'main/bulletins.html'
    context_object_name = 'bulletins'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}


class BulletinShowAndUpdatePage(DataMixin, UpdateView):
    model = Bulletin
    template_name = 'main/bulletin_create_update.html'
    form_class = BulletinCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context(), 'current_bulletin': self.object}



class BulletinCreatePage(DataMixin, CreateView):
    model = Bulletin
    template_name = 'main/bulletin_create_update.html'
    form_class = BulletinCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}

    # This method is called when we submit our form and all fields we validated
    # but our new model instance has not been saved yet:
    def form_valid(self, form):
        # QuerySet of selected questions:
        cleaned_data = form.cleaned_data['questions']
        # Getting the new bulletin instance with selected questions
        new_bulletin = form.save()

        for question in cleaned_data:
            question.bulletin = new_bulletin
            question.save()

        Question.objects.filter(bulletin__isnull=True).delete()

        return redirect('bulletins_all')



class UsersPage(DataMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'main/users.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context()}


class ResultsPage(DataMixin, ListView):
    pass


class AddQuestionAjax(View):
    def post(self, request):
        data = json.loads(request.body)
        if data:
            for index, question in enumerate(data):
                if 'type' in question and 'question' in question and 'answers' in question:
                    # question_type = int(question['type'])
                    # question_text = question['question']
                    # question_answers = question['answers']

                    new_question = Question.objects.create(
                        type=QuestionType.objects.get(pk=int(question['type'])),
                        question=question['question'],
                        answers={index: element for index, element in enumerate(question['answers'])}
                    )

                    if new_question:
                        return JsonResponse(data={'ok': 'Вопросы были успешно добавлены'}, status=201)

                return JsonResponse(data={'error': f'Вопрос под номером {index + 1} не имеет ответов'}, status=400)

            return JsonResponse(data={'error': 'Возникла ошибка получения данных...'}, status=400)
