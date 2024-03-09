import json
import secrets

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, TemplateView, UpdateView

from .forms import *
from .utils import *


def create_code(count: int, code_length: int) -> list[str]:

    res_codes = set()

    while len(res_codes) != count:
        res_codes.add(secrets.token_hex(code_length // 2))

    return [*res_codes]


def get_unique_codes(count: int, existing_codes: list[str]) -> list[str]:
    """
    Method to get unique codes for Anonymous with checking existing codes

    :param count: int: count of new codes for generating
    :param existing_codes: list[str]: list of existing codes in our model Anonym (codes of previously created Anonymous)
    """

    # Model._meta - a good instrument to get data about model structure and model fields:
    code_length = Anonym._meta.get_field('code').max_length

    # Generate new codes with specified count:
    new_codes = create_code(count=count, code_length=code_length)

    # Получим индексы new_codes для тех элементов, которые требуется изменить:

    # Getting list of indexes where indexes are for elements in new_codes which already in existing_codes:
    same_code_indexes = [new_codes.index(code) for code in new_codes if code in existing_codes]

    # So, if same_code_indexes list contains any element - we know that some codes are the same.
    while not same_code_indexes:
        # Create new codes by count of same elements:
        tmp_codes = create_code(len(same_code_indexes), code_length)
        # In loop, we change the new_codes[index]
        for index in same_code_indexes:
            new_codes[index] = tmp_codes.pop(0)

        same_code_indexes = [new_codes.index(code) for code in new_codes if code in existing_codes]

    return new_codes


# Create your views here.

class StartPage(View):
    """
    Class to display start page
    """

    def get(self, request):
        if self.request.user and self.request.user.is_authenticated:
            return redirect('home')

        return render(self.request, 'main/start_page.html')


class HomePage(LoginRequiredMixin, TemplateView):
    """
    Class to display home|start page
    """
    login_url = reverse_lazy('sign_in')
    template_name = 'main/home.html'


class AnonymConnectionPage(View):

    def get(self, request):
        """_summary_

        :param HttpRequest request: I don't know for what... View already has self.request
        """
        pass

    pass


class VotingPage(LoginRequiredMixin, ListView):
    model = Voting
    template_name = 'main/voting/voting.html'
    context_object_name = 'voting'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Voting.objects.all()

        return Voting.objects.filter(memberslist__user=self.request.user)


class VotingCreatePage(StaffRequiredMixin, CreateView):
    model = Voting
    template_name = 'main/voting/voting_creation.html'
    form_class = VotingCreationForm

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        new_voting = form.save()
        if cleaned_data['is_open']:

            members: list[MembersList] = []
            for user in cleaned_data['users']:
                members.append(MembersList(user=user, voting=new_voting))

            # Bulk_create() method gives an opportunity to create in one request more than one records in db from
            MembersList.objects.bulk_create(members)

        # Getting the existing codes from Anonym model:
        existing_anonymous_codes = [*Anonym.objects.all().values_list('code', flat=True)]

        # Getting anonymous cont from form:
        count_of_anonymous = int(cleaned_data['anonymous'])

        # Initialize new list with fresh and unique codes for creating Anonym-s:
        new_unique_codes = get_unique_codes(count_of_anonymous, existing_anonymous_codes)

        list_of_anonymous = []
        for code in new_unique_codes:
            list_of_anonymous.append(Anonym(voting=new_voting, code=code))

        Anonym.objects.bulk_create(list_of_anonymous)
        super().form_valid(form)
        return redirect('voting')


class VotingShowAndUpdatePage(StaffRequiredMixin, UpdateView):
    model = Voting
    template_name = 'main/voting/voting_creation.html'
    form_class = VotingCreationForm


class BulletinsListPage(StaffRequiredMixin, ListView):
    model = Bulletin
    template_name = 'main/bulletins/bulletins.html'
    context_object_name = 'bulletins'


class BulletinShowAndUpdatePage(StaffRequiredMixin, UpdateView):
    model = Bulletin
    template_name = 'main/bulletins/bulletin_crud.html'
    form_class = BulletinForm

    def form_valid(self, form):
        if 'confirm_update' in self.request.POST:
            questions = self.request.POST.getlist('questions')
            self.object = form.save()

            # We need to add new added questions which we got in questions and
            # delete other question were bulletin_id is null:
            # TODO: Add checking that lst contains any updated objects:
            if not Question.objects.filter(pk__in=questions, bulletin__isnull=True).update(bulletin=self.object):
                raise HttpResponseBadRequest(
                    'Не удалось назначить выбранный вопросы... Пожалуйста, повторите попытку позже')

            # Other questions which are not in use we need to delete from DATAbase:
            # In next time, we can add this as a feacher: 
            Question.objects.filter(bulletin__isnull=True).delete()

            # Call the same method from super() class:
            # It is a good practice when we overwrite the standard methods of any class:
            super().form_valid(form)
        elif 'confirm_delete' in self.request.POST:
            self.object.delete()

        return redirect('bulletins_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_bulletin_pk = self.object.pk
        current_bulletin_title = self.object.title
        return {**context,
                'bulletin_id': current_bulletin_pk,
                'page_title': f'Бюллетень №{current_bulletin_pk}',
                'second_title': f'Бюллетень №{current_bulletin_pk}. {current_bulletin_title}',
                'method': 'update_delete'}


class BulletinCreatePage(StaffRequiredMixin, CreateView):
    model = Bulletin
    template_name = 'main/bulletins/bulletin_crud.html'
    form_class = BulletinForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context,
                'page_title': 'Создание бюллетени',
                'second_title': 'Создание бюллетени'}

    # This method is called when we submit our form and all fields we validated
    # but our new model instance has not been saved yet:
    def form_valid(self, form):
        questions = self.request.POST.getlist('questions')

        new_bulletin = form.save()

        # TODO: Add lst variable checking to be sure that update operation was successful !
        if not Question.objects.filter(pk__in=questions).update(bulletin=new_bulletin):
            # HttpResponseBadRequest error - it's the 400 code error
            raise HttpResponseBadRequest(
                'Не удалось назначить выбранные вопросы... Пожалуйста, повторите попытку позже')

        Question.objects.filter(bulletin__isnull=True).delete()

        return redirect('bulletins_all')


class ResultsPage(ListView):
    pass


class AddQuestionAjax(View):
    def post(self, request):
        data = json.loads(request.body)

        if not data:
            return JsonResponse(data={'error': 'Возникла ошибка получения данных...'}, status=400)

        questions_to_create = []
        for index, question in enumerate(data):
            if question['type'] == '' or not question['type'].isdigit():
                return JsonResponse(data={'error': f'Вопрос под номером {index + 1} не имеет типа вопроса'},
                                    status=400)

            if question['question'].strip() == '':
                return JsonResponse(data={'error': f'Вопрос под номером {index + 1} не имеет заголовка'},
                                    status=400)

            if not question['answers']:
                return JsonResponse(data={'error': f'Вопрос под номером {index + 1} не имеет ответов'},
                                    status=400)

            questions_to_create.append(
                Question(type=QuestionType.objects.get(pk=int(question['type'])),
                         question=question['question'], answers=question['answers'])
            )

        if Question.objects.bulk_create(questions_to_create):
            return JsonResponse(data={'ok': 'Вопросы были успешно добавлены'}, status=201)


def handler400(request, exception=None):
    """
    This is our custom 400 error handler method.
    :param request: HttpRequest instance
    :param exception: Message in HttpResponseBadRequest()
    """

    return render(request, 'error_page.html', context=exception, status=400)
