from django import template

from ..models import Question

register = template.Library()

menu = [
    {'id': 1, 'name': 'Голосования', 'url_name': 'voting_all'},
    {'id': 2, 'name': 'Бюллетени', 'url_name': 'bulletins_all'},
    {'id': 3, 'name': 'Результаты', 'url_name': 'results'},
    {'id': 4, 'name': 'Пользователи', 'url_name': 'users:all-users'},
]


@register.inclusion_tag(filename='main/tags_pages/questions_with_answers_for_form.html')
def questions_with_bulletin(got_id=None):
    return {'questions': Question.objects.filter(bulletin_id=got_id)}


@register.inclusion_tag(filename='main/tags_pages/questions_with_answers_for_form.html')
def questions_without_bulletin():
    return {'questions': Question.objects.filter(bulletin__isnull=True)}


@register.inclusion_tag(filename='main/tags/menu_tag.html')
def get_menu(current_user):
    return {'main_menu': [menu[0], menu[2]] if not current_user.is_staff else menu, 'user': current_user}
