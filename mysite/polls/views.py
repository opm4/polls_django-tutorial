from django.db import models
from django.shortcuts import get_object_or_404, render 
from django.http import HttpResponse, HttpResponseRedirect, response, Http404
from django.template import context, loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        ''' 
        Returns the last five published questions. (not including those set up to be
        published in the future). 
        '''
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#             }
#     return render(request, 'polls/index.html', context)
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'
    
# def details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/details.html', {'question': question})
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after succsessfully dealing
        # with a POST data. This prevents data from being posted twice if 
        # a user hits Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
    