from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from forum.models import Answer, Question, Tag
from forum.forms import QuestionCreateForm, SearchForm, AnswerCreateForm
from users.models import User
import re


# Create your views here.

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


class HomeView(ListView):
    model = Question
    template_name = 'forum/question_list.html'
    paginate_by = 50

    def get_queryset(self):
        input_text = self.request.GET.get('q', '')
        if input_text.startswith('user:'):
            parts = input_text.split(':')

            return Question.objects.filter(user__username__icontains=parts[1])
        elif input_text.startswith('[') and input_text.endswith(']'):
            return Question.objects.filter(tag__name__icontains=input_text[1:-1])

        return Question.objects.filter(title__icontains=input_text)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class QuestionDetailView(DetailView):
    model = Question

    def get(self, request, *args, **kwargs):
        self.object: Question = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm

    success_url = reverse_lazy('forum:home')
    template_name = 'forum/question_add.html'

    def form_valid(self, form, ):
        self.object: Question = form.save(self.request.user, commit=False)
        return HttpResponseRedirect(self.get_success_url())


class StaffRequiredMixin:
    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()
        return Question.objects.filter(user=self.request.user)


class QuestionUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'text']
    template_name = 'forum/question_edit.html'


class QuestionDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('forum:home')


@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answer = Answer(user=request.user, question=question)

    if request.method == "POST":
        form = AnswerCreateForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            return redirect(question)
    else:
        form = AnswerCreateForm(instance=answer)
    return render(request, 'forum/question_detail.html', {'question': question, 'form': form})
