from django.urls import re_path
from .consumer import VoteConsumer

websocket_urlpatterns = [
    # Here we need to specify the url with using re_path (reg. expressions) to our consumer:
    # $ - means that full match should be;
    # (?P<param_name>) - specify the param
    # [-\w] - means, that for our param we could use - and some other symbols from the meaning of \w
    # + - after [set of symbols to use] means that number of symbols can be different
    re_path(r'ws/voting-online/url=(?P<vote_url>[-\w]+)/$', VoteConsumer.as_asgi())
]
