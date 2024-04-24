from django.db.models import F
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse



from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm, ChoiceFormSet

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=Question())
        if form.is_valid() and formset.is_valid():
            question = form.save()
            choices = formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            return redirect('polls:detail', question_id=question.id)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet(instance=Question())
    return render(request, 'polls/create_question.html', {'form': form, 'formset': formset})

def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), can_delete=True, extra=0)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            choices = formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            return redirect('polls:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question)
    return render(request, 'polls/update_question.html', {'form': form, 'formset': formset, 'question': question})

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('polls:index')
    return render(request, 'polls/delete_question.html', {'question': question})


def delete_choice(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=choice_id)
    if request.method == 'POST':
        choice.delete()
        return redirect('polls:update_question', question_id=question.id)
    return render(request, 'polls/delete_choice.html', {'question': question, 'choice': choice})