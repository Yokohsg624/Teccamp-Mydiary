from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="ユーザー名", max_length=20)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)
