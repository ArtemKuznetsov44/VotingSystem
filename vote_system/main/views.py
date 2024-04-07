import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, TemplateView, UpdateView
from django.db.models import Q

from users.models import User
from .forms import *
from .utils import *


class StartPage(View):
    """ Class to display start page with login ways """

    def get(self, request):
        if self.request.user and self.request.user.is_authenticated:
            return redirect('home')

        return render(self.request, 'main/start_page.html')


class HomePage(LoginRequiredMixin, TemplateView):
    """ Class to display home/main page where user is authenticated """
    login_url = reverse_lazy('sign_in')
    template_name = 'main/home.html'


class VotingListPage(LoginRequiredMixin, ListView):
    """ Class to display page with voting list """
    model = Voting
    template_name = 'main/voting/voting_list.html'
    context_object_name = 'voting'

    def get_queryset(self):
        """ Method to return voting-objects for staff and non-staff users """
        if self.request.user.is_staff:
            return Voting.objects.all()

        return Voting.objects.filter(userparticipant__user=self.request.user)


class VotingCreationPage(StaffRequiredMixin, CreateView):
    model = Voting
    template_name = 'main/voting/voting_creation.html'
    form_class = VotingCreationForm
    success_url = reverse_lazy('voting-list')

    def form_valid(self, form):
        """ Method starts only if the form is valid """

        data = form.cleaned_data

        if not data:
            form.add_error(field=None, error='Системе не удалось получить данные с формы')
            return super().form_invalid(form=form)

        try:
            new_voting_obj = Voting.objects.create(
                url=get_unique_url(data['is_open']),
                title=data['title'],
                is_open=data['is_open'],
                description=data['description']
            )

            if not new_voting_obj:
                raise RuntimeError("При создании объекта голосования произошла ошибка")

            bulletins_for_update = data['bulletins']
            selected_bulletins = bulletins_for_update.update(voting=new_voting_obj)

            if not selected_bulletins:
                raise RuntimeError('При назначении бюллетеней для голосования произошла ошибка')

            if new_voting_obj.is_open:
                # Create the list of UserParticipant objects:
                user_participants = [UserParticipant(voting=new_voting_obj, user=user) for user in data['users']]
                # Use bulk_create method to create new user participants in one request:
                participants = UserParticipant.objects.bulk_create(user_participants)

                if not participants:
                    raise RuntimeError('При назначении участников голосования произошла ошибка')
            else:
                anonyms = [
                    Anonym(unique_code=get_unique_code(), voting=new_voting_obj)
                    for _ in range(data['anonyms'])
                ]

                anonyms = Anonym.objects.bulk_create(anonyms)
                if not anonyms:
                    raise RuntimeError('При назначении/создании анонимных участников произошла ошибка')

            return redirect(self.success_url)
        except RuntimeError as ex:
            # form.add_error - method to add errors into form, field=None means that we add non_field error:
            form.add_error(field=None, error=ex)
            # Method to render the form with errors (field errors or non_field errors):
            return super().form_invalid(form=form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulletin_form'] = AddBulletinForm()
        context['bulletins'] = Bulletin.objects.filter(voting__isnull=True)
        context['method'] = 'create'
        context['title'] = 'Создание голосования'
        return context


class VotingShowUpdateAndDeletePage(StaffRequiredMixin, UpdateView):
    """ View for show and update one voting instance """
    model = Voting
    template_name = 'main/voting/voting_creation.html'
    form_class = VotingCreationForm
    slug_field = 'url'
    slug_url_kwarg = 'url'
    success_url = reverse_lazy('voting-list')

    def get_form(self, form_class=None):
        """ Return an instance of the form to be used in this view. """
        form = super().get_form(form_class=self.form_class)
        form.fields['bulletins'].queryset = Bulletin.objects.filter(Q(voting__isnull=True) | Q(voting=self.object))
        form.fields['bulletins'].initial = form.fields['bulletins'].queryset.filter(voting=self.object)
        return form

    def get_initial(self):
        """ Return the initial data to use for forms on this view. """
        initial = super().get_initial()

        if self.object.is_open:
            participants = UserParticipant.objects.filter(voting=self.object)
            users = [participant.user for participant in participants]
            initial['users'] = users
        else:
            initial['anonyms'] = self.object.anonym_set.all().count()
            print(initial['anonyms'])
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            if not data:
                raise RuntimeError('Не удалось получить данные с формы')

            action = self.request.POST.get('action')

            if not action:
                raise RuntimeError('Не удалось определить действие для формы')

            if action == 'delete':
                if not self.object.delete():
                    raise RuntimeError('Произошла ошибка при удалении голосования')
            elif action == 'update':
                # If user change the type of voting:
                if self.object.is_open != data['is_open']:
                    # In case when our voting was open, but became closed:
                    if self.object.is_open:
                        # Need to delete UserParticipants for current voting and create new anonyms for it:
                        if not self.object.userparticipants_set.delete():
                            raise RuntimeError('Не удалось переназначить участников для голосования')

                        anonyms = [Anonym(unique_code=get_unique_code(), voting=self.object) for _ in
                                   range(data['anonyms'])]
                        if not Anonym.objects.bulk_create(anonyms):
                            raise RuntimeError('Не удалось переназначить участников для голосования')
                    else:
                        # In case when our voting was closed, but became open:
                        if not self.object.anonym_set.delete():
                            raise RuntimeError('Не удалось переназначить участников для голосования')

                        participants = [UserParticipant(user=user, voting=self.object) for user in data['users']]
                        if not UserParticipant.objects.bulk_create(participants):
                            return RuntimeError('Не удалось переназначить участников для голосования')

                # Get current bulletins objects for voting:
                current_bulletins = self.object.bulletin_set.all()
                # If their not equals to new user checkout bulletins:
                if current_bulletins != data['bulletins']:
                    # Unbound current bulletins:
                    res_for_unbound = current_bulletins.update(voting=None)
                    # And bound new bulletins objects for current voting:
                    res_for_bound = data['bulletins'].update(voting=self.object)
                    if not res_for_unbound or not res_for_bound:
                        raise RuntimeError('Произошла ошибка при попытке переназначения бюллетеней для голосования')

            return redirect(self.success_url)

        except RuntimeError as ex:
            form.add_error(field=None, error=ex)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulletin_form'] = AddBulletinForm()
        context['method'] = 'update_delete'
        context['title'] = 'Просмотр/обновление голосования'
        return context


class BulletinsFetchView(View):
    """ View to work with fetch-request during bulletins creation or deleting """

    def delete(self, request):
        data = json.loads(request.body)
        ''' data = {'to_delete': <bulletin_pk/id>:int} '''
        if not data:
            return HttpResponseBadRequest('Invalid or no data provided')

        if get_object_or_404(Bulletin, pk=int(data['to_delete'])).delete():
            return HttpResponse(status=200)

        return HttpResponseBadRequest('Error in deleting bulletin')

    def post(self, request):
        data = json.loads(request.body)

        if not data:
            return JsonResponse(data='No data was received', status=400)

        bulletins_to_create = []

        for index, bulletin in enumerate(data):
            if bulletin['type'] == '' or bulletin['type'] not in ['single', 'multiple']:
                return JsonResponse(
                    data={'error': f'В бюллетени под номером {index + 1} не указан типа вопроса'},
                    status=400
                )

            if bulletin['question'].strip() == '':
                return JsonResponse(
                    data={'error': f'Бюллетень под номером {index + 1} не содержит вопроса'},
                    status=400
                )

            if not bulletin['answers']:
                return JsonResponse(
                    data={'error': f'Бюллетень под номером {index + 1} не имеет ответов'},
                    status=400
                )

            # if any([element.strip() for element in bulletin['answers']])

            bulletins_to_create.append(
                Bulletin(
                    question=bulletin['question'],
                    type=bulletin['type']
                )
            )

        created_bulletins = Bulletin.objects.bulk_create(bulletins_to_create)

        answers_to_create = []
        for bulletin_obj, data_element in zip(created_bulletins, data):
            # When we need to append list with another list, we should use extend method:
            answers_to_create.extend(
                [Answer(text=element, bulletin=bulletin_obj) for element in data_element['answers']])

        created_answers = Answer.objects.bulk_create(answers_to_create)

        if created_answers and created_bulletins:
            return JsonResponse(data={'ok': 'Бюллетени и ответы к ним были добавлены в базу'}, status=201)


class ResultsListPage(StaffRequiredMixin, ListView):
    pass


def handler400(request, exception=None):
    """
    This is our custom 400 error handler method.
    :param request: HttpRequest instance
    :param exception: Message in HttpResponseBadRequest()
    """

    return render(request, 'error_page.html', context=exception, status=400)
