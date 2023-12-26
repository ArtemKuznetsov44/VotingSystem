menu = [
    {'id': 1, 'name': 'Голосования', 'url_name': 'voting_all'},
    {'id': 2, 'name': 'Бюллетени', 'url_name': 'bulletins_all'},
    {'id': 3, 'name': 'Результаты', 'url_name': 'results'},
    {'id': 4, 'name': 'Пользователи', 'url_name': 'users'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = [menu[0], menu[2]] if not self.request.user.is_staff else menu
        return context
