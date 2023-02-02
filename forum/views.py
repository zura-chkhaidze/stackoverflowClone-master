from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from forum.models import Answer, Question, Tag
from forum.forms import QuestionCreateForm, SearchForm, AnswerCreateForm
from users.models import User

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
        parts = input_text.split(':')
        if len(parts) > 1:
            return Question.objects.filter(user__username__icontains=parts[1])
        elif input_text.startswith('[') and input_text.endswith(']'):
            return Question.objects.filter(tag__name__icontains=input_text.replace('[', '').replace(']', ''))

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


class AnswerDetailView(DetailView):
    model = Question

   
class TagDetailView(DetailView):
    model = Tag
    fields = [
        'name'
    ]
    
    template_name = 'forum/question_list.html'

   


# def create_question_view(request):
#     if request.method == 'GET':
#         return render(
#             request, 
#             'forum/question_add.html', 
#             {
#                 'form': QuestionCreateForm()
#             }
#         )

#     print(request.POST)
#     form = QuestionCreateForm(request.POST)

#     if form.is_valid():
#         form.save()
#         return redirect('forum:home')

#     return render(
#         request, 
#         'forum/question_add.html', 
#         {
#             'form': form
#         }
#     )

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question

    fields = [
        'title', 'text',
    ]
    success_url = reverse_lazy('forum:home')
    template_name = 'forum/question_add.html'


    def form_valid(self, form,):
        self.object: Question = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)





class StaffRequiredMixin:
    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()
        return Question.objects.filter(user=self.request.user)


class QuestionUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'text' ,'tags']
    template_name = 'forum/question_edit.html'


class QuestionDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('forum:home')




class AnswerCreateView(StaffRequiredMixin,LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['text', 'question']
    success_url = reverse_lazy('forum:home')
    template_name = 'forum/answer_add.html'

    def form_valid(self, form):
        self.object: Answer = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)

