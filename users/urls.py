from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from users.views import IndexView, LoginView, LogoutView, RegisterView, ProfileView

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]