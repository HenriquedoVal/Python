from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect  # , Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
                          'question': question,
                          'error_message': "You didn't selected a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # On success always return redirect for preventing doubling
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )


'''
# class IndexView will do this work
def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_questions': latest_questions
    }

    # Same way to do the same thing or what's going on behind
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    return render(request, 'polls/index.html', context)


# class DetailView...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Same way to do the same thing
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exists")

    return render(request, 'polls/detail.html', {'question': question})


# class ResultView...
def results(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''
