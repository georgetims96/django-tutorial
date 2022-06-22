from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'
  
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    # FIXME what does choice_set refer to
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't pick a choice",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    # FIXME N.B. should ALWAYS return an HTTPResponse
    # redirect after successfully dealing with POST. 
    # This prevents data from being submitted twice
    # if a user goes back.

    # FIXME figure out logic of reverse function here
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

  return HttpResponse(f"You're voting on question {question_id}")


