import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, TemplateView, UpdateView, DetailView
from django.db.models import Q, Count, Case, When, Value, BooleanField

from users.models import User
from .forms import *
from .utils import *


class StartPage(View):
    """ Class to display start page with login ways """

    def get(self, request):
        if self.request.user and self.request.user.is_authenticated:
            return redirect('voting-list')

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

        return Voting.objects.filter(userparticipant__user=self.request.user, status__in=['active', 'finished'])


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

            action = self.request.POST.get('action', )

            if not action:
                raise RuntimeError('Не удалось определить действие для формы')

            if action == 'delete':
                if not self.object.delete():
                    raise RuntimeError('Произошла ошибка при удалении голосования')
            elif action == 'update':
                if self.object.title != data['title']:
                    self.object.title = data['title']

                if self.object.description != data['description']:
                    self.object.description = data['description']

                if self.object.is_open:
                    if data['is_open'] is False:
                        #  Delete participants for current voting, because the status of voting was changed:
                        if not self.object.userparticipan_set.delete():
                            raise RuntimeError('Не удалось удалить текущих назначенных участников на голосование')

                    elif data['is_open'] is True and set(data['users']) != (
                            current_users_set := {participant.user for participant in
                                                  self.object.userparticipant_set.filter(voting=self.object)}):
                        # Cases when voting stay open, but users change users for current voting:
                        # current_users_set = set(current_users)
                        data_users_set = set(data['users'])

                        # With the symmetric_difference find elements  which are only in first set or only in second
                        # set but not in both at the same time (getting only difference elements):
                        difference = current_users_set.symmetric_difference(data_users_set)

                        if len(current_users_set) > len(data_users_set):
                            # Delete some user participant, because current let of them smaller and delete only
                            # difference element (means, that some users was unchecked):
                            self.object.userparticipant_set.filter(user__in=difference).delete()
                        elif len(current_users_set) < len(data_users_set):
                            # Create some new user participants for current voting, because some users have become
                            # checked:
                            new_user_participants = [UserParticipant(user=user, voting=self.object) for user in
                                                     difference]
                            if not UserParticipant.objects.bulk_create(new_user_participants):
                                raise RuntimeError('Не удалось добавить пользователей для текущего голосования')
                        elif len(current_users_set) == len(data_users_set):
                            for_remove = current_users_set.intersection(difference)
                            for_add = data_users_set.intersection(difference)

                            self.object.userparticipant_set.filter(user__in=for_remove).delete()
                            new_user_participants = [UserParticipant(user=user, voting=self.object) for user in for_add]

                            if not UserParticipant.objects.bulk_create(new_user_participants):
                                raise RuntimeError('Не удалось переназначить пользователь для текущего голосования')
                else:
                    # Cases, when current voting status is closed:
                    if data['is_open'] is True:
                        # Delete all anonyms for current voting, because the status was changed:
                        if not self.object.anonym_set.delete():
                            raise RuntimeError('Не удалось удалить текущих анонимных участников для голосования')
                    if data['is_open'] is False and data['anonyms'] != (
                            current_anonyms_count := self.object.anonym_set.all().count()):
                        # Cases when user can increase or decrease the count of anonyms:

                        # Find the difference count:
                        difference_count = abs(current_anonyms_count - data['anonyms'])

                        if current_anonyms_count > data['anonyms']:
                            # If current count is bigger than should be now, delete some anonyms with slices:
                            self.object.anonym_set.all()[:difference_count].delete()
                        else:
                            # When current count is smaller, we should create new anonyms for voting:
                            new_anonyms = [Anonym(unique_code=get_unique_code(), voting=self.object) for _ in
                                           range(difference_count)]
                            if not Anonym.objects.bulk_create(new_anonyms):
                                raise RuntimeError(
                                    'Не удалось создать новых анонимных участников для текущего голосования')

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

            # Save possible changes:
            self.object.save()
            return redirect(self.success_url)

        except RuntimeError as ex:
            form.add_error(field=None, error=ex)
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulletin_form'] = AddBulletinForm()
        context['method'] = 'update_delete'
        context['title'] = 'Просмотр/обновление голосования'
        return context


class VotingResultView(TemplateView):
    template_name = 'main/voting/voting_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_vote'] = get_object_or_404(Voting, url=kwargs.get('url'))

        # Получаем бюллетени с ответами и голосами

        bulletin_with_answers = Bulletin.objects.filter(voting=context['current_vote']).prefetch_related(
            'answer_set').annotate(
            total_votes=Count('userbulletinanswer')
        )

        results = {}

        for bulletin in bulletin_with_answers:
            # Gets all available answers for current bulletin:
            all_available_answers = bulletin.answer_set.all()

            # Annotate our answers with count of votes by user for them:
            answers_info = all_available_answers.annotate(
                votes_count=Count('userbulletinanswer__id')
            ).order_by('id')

            # Make aggregation for answers, and getting the max count of votes for bulletin answer:
            max_votes_count = answers_info.aggregate(max_votes=Count('userbulletinanswer__id'))['max_votes']
            max_votes_count = max_votes_count if max_votes_count > 0 else -1

            # Annotate our answers_info with 'max' column, where 'max' colum use case-when statement:
            answers_info = answers_info.annotate(
                max=Case(
                    When(votes_count=max_votes_count, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).values('id', 'text', 'votes_count', 'max')

            # Create the dictionary with information about answers for current bulletin:
            answers_dict = {
                answer['id']: {
                    'answer_text': answer['text'],
                    'votes_count': answer['votes_count'],
                    'percent': (
                        0 if answer['votes_count'] == 0 else answer['votes_count'] * 100 / bulletin.total_votes,
                        answer['max']
                    )
                }
                for answer in answers_info
            }

            # Получаем информацию о пользователях и их ответах
            votes_for_bulletin_with_users = bulletin.userbulletinanswer_set.select_related('user',
                                                                                           'answer').values_list(
                'user__first_name',
                'user__last_name',
                'user__father_name',
                'answer__text'
            )

            print(votes_for_bulletin_with_users)

            # Сохраняем результаты для текущего бюллетеня
            results[bulletin.pk] = {
                'question': bulletin.question,
                'total_count': bulletin.total_votes,
                'answers_info': answers_dict,
                'users_and_votes': votes_for_bulletin_with_users
            }

        context['results'] = results
        return context


class BulletinsFetchView(View):
    """ View to work with fetch-request during bulletins creation or deleting """

    def delete(self, request):
        data = json.loads(request.body)
        ''' data = {'to_delete': <bulletin_pk/id>:int} '''

        check_data_in_fetch(data)

        if get_object_or_404(Bulletin, pk=int(data['to_delete'])).delete():
            return HttpResponse(status=200)

        return HttpResponseBadRequest('Error in deleting bulletin')

    def post(self, request):
        data = json.loads(request.body)

        if not data:
            return JsonResponse(data='No data was received', status=400)

        voting_pk = int(value) if (value := data.pop('voting_pk', None)) else None
        bulletins_to_create = []

        # voting_pk = int(value) if (value := data.pop('voting_pk', None)) else None

        for bulletin_index, bulletin_data in data.items():
            if bulletin_data['type'] == '' or bulletin_data['type'] not in ['single', 'multiple']:
                return JsonResponse(
                    data={'error': f'В бюллетени под номером {bulletin_index + 1} не указан типа вопроса'},
                    status=400
                )

            if bulletin_data['question'].strip() == '':
                return JsonResponse(
                    data={'error': f'Бюллетень под номером {bulletin_index + 1} не содержит вопроса'},
                    status=400
                )

            if not bulletin_data['answers']:
                return JsonResponse(
                    data={'error': f'Бюллетень под номером {bulletin_index + 1} не имеет ответов'},
                    status=400
                )

            bulletins_to_create.append(
                Bulletin(
                    question=bulletin_data['question'],
                    type=bulletin_data['type'],
                    voting_id=voting_pk if voting_pk else None
                )
            )

        created_bulletins = Bulletin.objects.bulk_create(bulletins_to_create)

        answers_to_create = []
        for bulletin_obj, data_element in zip(created_bulletins, data.values()):
            # When we need to append list with another list, we should use extend method:
            answers_to_create.extend(
                [Answer(text=element, bulletin=bulletin_obj) for element in data_element['answers']])

        created_answers = Answer.objects.bulk_create(answers_to_create)

        if created_answers and created_bulletins:
            answers_by_bulletin_pk = {}
            '''
            answers_by_bulletin_pk = {
                'bulletin_pk': {'a}
            }
            '''

            for answer in created_answers:
                if answer.bulletin_id not in answers_by_bulletin_pk:
                    answers_by_bulletin_pk[answer.bulletin_id] = {answer.pk: answer.text}
                else:
                    answers_by_bulletin_pk[answer.bulletin_id].update({answer.pk: answer.text})

            bulletins_data = {
                bulletin.pk: {
                    'question': bulletin.question,
                    'type': bulletin.type,
                    'answers': answers_by_bulletin_pk[bulletin.pk]
                }
                for bulletin in created_bulletins
            }
            '''
            bulletins_data = {<bulletin_id>: {'type': <type>, 'question': <question> 'answers': [answer_text1, answer_text2, ...]} }
            '''
            return JsonResponse(
                data={
                    'ok': 'Бюллетени и ответы к ним были добавлены в базу',
                    'bulletins_data': json.dumps(bulletins_data)
                }, status=201
            )


class ActiveVoting(TemplateView):
    # login_url = reverse_lazy('users:sign_in')
    template_name = 'main/voting/active_vote.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = get_object_or_404(Voting, url=kwargs.get('url'))
        # Gets info about current voting process:
        context['vote'] = voting

        context['all_bulletins_for_vote'] = voting.bulletin_set.all().prefetch_related(
            'answer_set').annotate(
            total_votes=Count('userbulletinanswer')
        )

        answered_bulletins_id_by_user = [bulletin_id for bulletin in context['all_bulletins_for_vote'] for bulletin_id
                                         in bulletin.userbulletinanswer_set.filter(
                user_id=self.request.user.pk).values_list('bulletin_id', flat=True).distinct()]

        print('Answered bulletins by user - ', answered_bulletins_id_by_user)

        context['for_user_bulletins'] = context['all_bulletins_for_vote'].filter(
            Q(active_status=True) & ~Q(id__in=answered_bulletins_id_by_user)).prefetch_related('answer_set')

        print('Bulletin objects to for display for user - ', context['for_user_bulletins'])

        # Main dict to save results:
        results = {}

        for bulletin in context['all_bulletins_for_vote']:
            # Получаем все доступные ответы для текущего бюллетеня
            all_available_answers = bulletin.answer_set.all()

            # Annotate our bulletin answers with counts of votes for them:
            answers_info = all_available_answers.annotate(
                votes_count=Count('userbulletinanswer__id')
            ).order_by('id').values('id', 'text', 'votes_count')

            # Create the dictionary with information about bulletin answers:
            answers_dict = {
                answer['id']:
                    {
                        'answer_text': answer['text'],
                        'votes_count': answer['votes_count']
                    }
                for answer in answers_info
            }

            results[bulletin.pk] = {
                'bulletin_question': bulletin.question,
                'answers_info': answers_dict,
                'total_count': bulletin.total_votes
            }

        context['results'] = results
        context['bulletin_form'] = AddBulletinForm()
        return context


class ResultsListPage(ListView):
    context_object_name = 'finished_votes'

    def get_queryset(self):
        return Voting.objects.filter(status='finished')

    # def get(self, request, **kwargs):
    #     return HttpResponseBadRequest('Погуляй, страницы пока нет!')


def handler400(request, exception=None):
    """
    This is our custom 400 error handler method.
    :param request: HttpRequest instance
    :param exception: Message in HttpResponseBadRequest()
    """

    return render(request, 'error_page.html', context=exception, status=400)
