from .forms import QuestionCreateForm


def get_context_data(request):
    context = {
        'add_question_ajax': QuestionCreateForm()
    }
    return context
