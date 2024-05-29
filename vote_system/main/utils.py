import secrets

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseBadRequest


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'users:sign_in'

    def test_func(self):
        return self.request.user.is_staff


def get_unique_code(code_len: int = 15) -> str:
    # We divide code_len on 1.3 because 1 byte contains in average 1.3 symbols
    # secrets.token_hex(nbytes) - has one param - the count of bytes
    return secrets.token_urlsafe(int(code_len / 1.3))


def get_unique_url(is_open: bool = True, code_len: int = 8) -> str:
    unique_code = get_unique_code(8)
    return f'vote-{unique_code}'


def check_data_in_fetch(body_data):
    """ Simple method to check that data in fetch exists and data is valid """
    if not body_data:
        return HttpResponseBadRequest('Invalid or no data provided')
