from django.urls import path, reverse_lazy
from users.views import LogoutView, LoginView, RegisterView,ProfileView

app_name = 'users'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('signup/', RegisterView.as_view(), name='auth-signup'),
    path('profile/', ProfileView.as_view(), name='users-profile'),
]
