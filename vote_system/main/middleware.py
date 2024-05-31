from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Anonym

@database_sync_to_async
def get_anonym_user(unique_code):
    """ Method to get anonym user from database by its unique code """
    try:
        return Anonym.objects.get(unique_code=unique_code)
    except Anonym.DoesNotExist:
        return None


class AnonymAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):

        if scope.get('user') and not isinstance(scope.get('user'), AnonymousUser):
            return await super().__call__(scope, receive, send)

        # query_sting - it is the part of url which contains get-params - all, after <?>, for example:
        # /url/?voting=<voting_id>&user=<user_id>, so query_string = 'voting=id&user=id'
        query_string = scope.get('query_string', b'').decode('utf-8')
        # parse_qs() function get query_string and return the dictionary => {'voting': [id], 'user': [id]}
        query_params = parse_qs(query_string)
        unique_code = query_params.get('unique_code', [None])[0]

        if unique_code:
            # unique_code = unique_code
            anonym_user = await get_anonym_user(unique_code)

            if anonym_user:
                scope['user'] = anonym_user
            else:
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
