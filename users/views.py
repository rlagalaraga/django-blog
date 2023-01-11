from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User

# Create your views here.
class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get(self, request):
        return render(request, self.template_name)

class RegisterView(TemplateView):
    template_name = 'users/register.html'

    def get(self, request):
        form = RegisterForm(request.POST)
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            email = request.POST['email']
            password = request.POST['password2']
            
            user = authenticate(request, email=email, password=password)
            return redirect('users:index')
        
        else:
            form = RegisterForm(request.POST)
            return render(request, 'users/register.html', {'form': form})

class LoginView(TemplateView):

    template_name = 'users/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request,'users/login.html', {'form' : form})

    def post(self, request):
        form = LoginForm(request.POST)

        #import pdb; pdb.set_trace()

        if form.is_valid():
            
            #passes email and pass, and authenticates it
            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Successfuly Logged In!')
                return HttpResponseRedirect(reverse_lazy('users:index'))
            else:
                form = LoginForm(request.POST)
                return render(request, 'users/login.html', {'form' : form})
        
        else:
            return render(request, 'users/login.html', {'form': form})

class ProfileView(TemplateView):
    template_name='users/profile.html'

    #gets posts of user logged in and profile details of user
    def get(self, request):
        profile = User.objects.get(id=request.user.id)
        context = {
            'profile' : profile
        }
        return render(request, self.template_name, context)

def LogoutView(request):
    logout(request)
    return redirect('users:index')