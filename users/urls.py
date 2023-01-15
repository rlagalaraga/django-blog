from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from users.views import IndexView, LoginView, LogoutView, RegisterView, ProfileView, ModifyProfileView, followToggle

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('modifyProfile/', ModifyProfileView.as_view(), name='modifyProfile'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('followToggle/<int:id>/', followToggle, name='followToggle')
]