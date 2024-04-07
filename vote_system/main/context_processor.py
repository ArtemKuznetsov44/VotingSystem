from .forms import AddBulletinForm


def get_context_data(request):
    context = {
        'add_bulletin_ajax': AddBulletinForm(),
    }
    return context
