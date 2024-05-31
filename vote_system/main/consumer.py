import json
from asgiref.sync import async_to_sync
from collections import namedtuple
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import Bulletin, UserBulletinAnswer, Voting, Anonym
from django.core.exceptions import ObjectDoesNotExist

# Logic:
'''
User can send:
1. Dict with answers for bulletins: {bulletin_id: [answer]}
'''


class VoteConsumer(WebsocketConsumer):
    Consumer = namedtuple('Consumer', ['human_name', 'username', 'channel_name'])
    consumers = {}
    admins = {}
    anonyms = {}
    current_voting = None

    @classmethod
    def set_current_voting(cls, current_voting):
        cls.current_voting = current_voting

    def connect(self):
        user = self.scope['user']
        print('USER - ', type(user))

        # Prepare two groups with different name:
        self.vote_group_as_name = self.scope['url_route']['kwargs']['vote_url']
        # # self.vote_group_as_name_for_admins = self.vote_group_as_name_for_all + '_admins'

        if isinstance(user, get_user_model()):

            if user.is_staff:
                self.set_current_voting(Voting.objects.get(url=self.vote_group_as_name))

                if self.current_voting.status != 'active':
                    self.current_voting.status = 'active'
                    self.current_voting.save()

            elif not self.current_voting or self.current_voting.status != 'active':
                self.close()
            else:
                if str(user.pk) not in self.consumers:
                    self.consumers[str(user.pk)] = self.Consumer(
                        f'{user.last_name} {user.first_name} {user.father_name}',
                        user.username,
                        self.channel_name
                    )
        else:
            self.anonyms[str(user.pk)] = user.unique_code

        # group_add() method in object channel_layer get two arguments: 1 - group_name and 2 - object.channel_name
        async_to_sync(self.channel_layer.group_add)(
            self.vote_group_as_name, self.channel_name
        )

        self.accept()

        print('Current group - ', self.vote_group_as_name, '; ', 'Current consumers - ', self.consumers)
        async_to_sync(self.channel_layer.group_send)(
            self.vote_group_as_name,
            {'type': 'update.connected.list', 'current_consumers': self.consumers}
        )

    def disconnect(self, close_code):
        self.consumers.pop(str(self.scope['user'].pk), None)
        # self.admins.pop(str(self.scope['user'].pk), None)

        async_to_sync(self.channel_layer.group_send)(
            self.vote_group_as_name, {
                'type': 'update.connected.list', 'current_consumers': self.consumers}
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.vote_group_as_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Code to handle the event, when admin make bulletin active or deactivate it:
        if 'bulletin_pk' in text_data_json:
            bulletin_pk = int(text_data_json['bulletin_pk'])
            # Try to find bulletin object by pk:
            try:
                bulletin = Bulletin.objects.get(pk=bulletin_pk)
            except Bulletin.DoesNotExist:
                self.send(text_data=json.dumps(
                    {'admin-error': f'Бюллетень с идентификатором {bulletin_pk} не была найдена...'}))
                return

            data = {}

            if bulletin.active_status:
                bulletin.active_status = False
            else:
                bulletin.active_status = True
                data.update({
                    'question': bulletin.question,
                    'type': bulletin.type,
                    'answers': [[answer.pk, answer.text] for answer in bulletin.answer_set.all()]
                })

            data['bulletin_pk'] = bulletin_pk

            bulletin.save()

            # Users id, who has already answered for current bulletin:
            answered_user = set(
                map(str, UserBulletinAnswer.objects.filter(
                    bulletin_id=bulletin_pk).values_list('user_id', flat=True))
            )
            all_clients = set(self.consumers.keys())

            not_answered_users = all_clients.difference(answered_user)
            not_answered_channel_names = [self.consumers[key].channel_name for key in not_answered_users]

            method = 'activate.bulletin' if len(data) > 1 else 'deactivate.bulletin'

            for channel_name in not_answered_channel_names:
                async_to_sync(self.channel_layer.send)(
                    channel_name,
                    {'type': method, 'bulletin_data': data}
                )

        elif 'user_bulletin_answers' in text_data_json:
            '''
            text_data_json['user_bulletin_answers'] = {'bulletin_id': <bulletin_id>, 'answers': [answer1, ..., ... ]}
            '''
            sender_id = int(self.scope['user'].pk)
            bulletin_data = text_data_json['user_bulletin_answers']
            if sender_id and bulletin_data:
                bulletin_pk = int(bulletin_data['bulletin_id'])
                answers_array = bulletin_data['answers']

                db_user_answers = [
                    UserBulletinAnswer(answer_id=int(answer), bulletin_id=bulletin_pk, user_id=sender_id)
                    for answer in answers_array
                ]

                dict_to_send = {}
                if not UserBulletinAnswer.objects.bulk_create(db_user_answers):
                    dict_to_send = json.dumps({
                        'error_answer_saving': {
                            'message': 'Не удалось сохранить ответы по данной бюллетени',
                            'bulletin_pk': bulletin_pk
                        }
                    })
                else:
                    dict_to_send = json.dumps({
                        'success_answer_saving': {
                            'bulletin_pk': bulletin_pk,
                            'answers': answers_array
                        }
                    })

                async_to_sync(self.channel_layer.group_send)(
                    self.vote_group_as_name,
                    {'type': 'send.saving.result', 'text_data': dict_to_send}
                )

        elif 'stop_voting' in text_data_json:
            # Get the actual voters count = active users - admins, because they do not have permission to vote:
            # voters_count = int(text_data_json['actual_voters_count']) - len(self.admins)

            self.current_voting.status = 'finished'
            # self.current_voting.actual_voters_count = voters_count
            self.current_voting.save()

            async_to_sync(self.channel_layer.group_send)(
                self.vote_group_as_name,
                {'type': 'vote.finishing', 'message_text': 'Голосование завершено'}
            )

    def send_saving_result(self, event):
        self.send(event['text_data'])

    def activate_bulletin(self, event):
        self.send(text_data=json.dumps(
            {'activate_bulletin': event['bulletin_data']}))

    def deactivate_bulletin(self, event):
        self.send(text_data=json.dumps(
            {'deactivate_bulletin': event['bulletin_data']}))

    def update_connected_list(self, event):
        if event.get('current_consumers', None):
            self.send(text_data=json.dumps(
                {'update_connections': event['current_consumers']}))

    def vote_finishing(self, event):
        self.send(text_data=json.dumps({'finish_message': event['message_text']}))
