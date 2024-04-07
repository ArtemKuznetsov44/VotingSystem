import secrets

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def get_unique_code(code_len: int = 15) -> str:
    # We divide code_len on 1.3 because 1 byte contains in average 1.3 symbols
    # secrets.token_hex(nbytes) - has one param - the count of bytes
    return secrets.token_urlsafe(int(code_len / 1.3))


def get_unique_url(is_open: bool = True, code_len: int = 8) -> str:
    unique_code = get_unique_code(8)
    return f'vote-{unique_code}'

# def create_code(count: int, code_length: int) -> list[str]:
#     res_codes = set()
#
#     while len(res_codes) != count:
#         res_codes.add(secrets.token_hex(code_length // 2))
#
#     return [*res_codes]
#
#
# def get_unique_codes(count: int, existing_codes: list[str]) -> list[str]:
#     """
#     Method to get unique codes for Anonymous with checking existing codes
#
#     :param count: int: count of new codes for generating
#     :param existing_codes: list[str]: list of existing codes in our model Anonym (codes of previously created Anonymous)
#     """
#
#     # Model._meta - a good instrument to get data about model structure and model fields:
#     code_length = Anonym._meta.get_field('code').max_length
#
#     # Generate new codes with specified count:
#     new_codes = create_code(count=count, code_length=code_length)
#
#     # Получим индексы new_codes для тех элементов, которые требуется изменить:
#
#     # Getting list of indexes where indexes are for elements in new_codes which already in existing_codes:
#     same_code_indexes = [new_codes.index(code) for code in new_codes if code in existing_codes]
#
#     # So, if same_code_indexes list contains any element - we know that some codes are the same.
#     while not same_code_indexes:
#         # Create new codes by count of same elements:
#         tmp_codes = create_code(len(same_code_indexes), code_length)
#         # In loop, we change the new_codes[index]
#         for index in same_code_indexes:
#             new_codes[index] = tmp_codes.pop(0)
#
#         same_code_indexes = [new_codes.index(code) for code in new_codes if code in existing_codes]
#
#     return new_codes
