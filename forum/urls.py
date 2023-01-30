from django.urls import path
from forum.views import AnswerCreateView, AnswerDetailView, HomeView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView
from . import views
app_name = 'forum'
urlpatterns = [
    path('about/', views.about, name="about"),
     path('contact/', views.contact, name="contact"),
    path('', HomeView.as_view(), name='home'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question/<int:pk>/edit/', QuestionUpdateView.as_view(), name='question-edit'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('ask/', QuestionCreateView.as_view(), name='question-add'),
    path('question/<int:pk>/', AnswerDetailView.as_view(), name='question-detail'),
    path('answer/', AnswerCreateView.as_view(), name='answer-add'),
]
