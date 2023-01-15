from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm, RegisterForm, UpdateUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import User
from posts.models import Post

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
            messages.success(request, 'Your account is now registered try logging in.')
            return redirect('posts:dashboard')
        
        else:
            form = RegisterForm(request.POST)
            messages.error(request, 'Invalid Input!')
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
                messages.success(request, 'Successfully Logged In!')
                return HttpResponseRedirect(reverse_lazy('posts:dashboard'))
            else:
                form = LoginForm(request.POST)
                messages.error(request, 'Please enter correct Email and Password!')
                return render(request, 'users/login.html', {'form' : form})
        
        else:
            messages.error(request, 'Please enter correct Email and Password!')
            return render(request, 'users/login.html', {'form': form})


class ProfileView(TemplateView):
    template_name='users/profile.html'

    #gets posts of user logged in and profile details of user
    def get(self, request, id):
        posts = Post.objects.filter(author=id)
        profile = get_object_or_404(User, id=id)
        isFollowed = False
        if profile.following.filter(id = request.user.id).exists():
            isFollowed = True
        context = {
            'posts' : posts,
            'profile' : profile,
            'isFollowed': isFollowed
        }
        return render(request, self.template_name, context)
    
def followToggle(request, id):
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    if user.following.filter(id = request.user.id).exists():
        user.following.remove(request.user)
    else:
        user.following.add(request.user)
    return HttpResponseRedirect(reverse('users:profile', args=[id]))

def LogoutView(request):
    logout(request)
    messages.success(request, 'Account Logged Out!')
    return redirect('posts:dashboard')

class ModifyProfileView(TemplateView):
    template_name='users/modifyProfile.html'

    def get(self, request):
        form = UpdateUserForm()
        return render(request, 'users/modifyProfile.html', {'form' : form})
    
    def post(self, request):
        #get profile of user currently logged in
        profileUser = User.objects.get(id=request.user.id)
        profile_form = UpdateUserForm(request.POST, request.FILES, instance=profileUser)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile has been updated successfully!')
            return redirect('users:profile')

        else:
            form = UpdateUserForm()
            messages.error(request, 'Invalid Input!')
            return render(request, 'users/modifyProfile.html', {'form' : form})

