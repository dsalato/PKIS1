from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import RegisterUserForm, ProfileUpdate
from .models import *
from django.urls import reverse, reverse_lazy
from django.views import generic


class RegisterView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:index')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class Profile(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'polls/profile.html'


class ProfileUpdate(UpdateView):
    model = User
    form_class = ProfileUpdate
    template_name = 'polls/profile_update.html'
    success_url = reverse_lazy('polls:profile')


class ProfileDelete(DeleteView):
    model = User
    template_name = 'polls/profile_delete.html'
    success_url = reverse_lazy('polls:login')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        if Question.objects.filter(id=question_id, user_vote=request.user):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'Вы уже сделали выбор'
            })
        else:
            question.user_vote.add(request.user)
            question.vote += 1
            question.save()
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
