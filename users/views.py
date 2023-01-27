from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView as DjangoLogoutView, LoginView as DjangoLoginView
from forum.models import Question
from users.models import User,Profile
from users.forms import UserCreationForm


# Create your views here.
class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('forum:home')


class LoginView(DjangoLoginView):
    next_page = reverse_lazy('forum:home')
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('forum:home')
    
class ProfileView(CreateView):
    model = Profile
    template_name = 'users/profile.html'
    success_url = reverse_lazy('forum:home')
    fields ='__all__'

   
    

   