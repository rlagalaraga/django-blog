from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput)
    first_name=forms.CharField(label='First Name')
    last_name=forms.CharField(label='Last Name')
    avatar = forms.ImageField(label='Profile Picture',widget=forms.FileInput)

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'avatar']

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', required=True, max_length=150)
    password = forms.CharField(label='Password', widget =forms.PasswordInput())

    field = (
        'email',
        'password'
    )

    def auth(self, request):

        auth_email = self.cleaned_data.get('email')
        pword = self.cleaned_data.get('password')
        return authenticate(request, email=auth_email, password=pword)