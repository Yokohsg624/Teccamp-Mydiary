from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import LoginForm
from django.urls import reverse_lazy

class AccountCreateView(generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/accounts_create.html'
    success_url = reverse_lazy('accounts:login')

class AccountCreateViewUsingMyForm(generic.CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/accounts_create.html'
    success_url = reverse_lazy('accounts:login')

class CustomAccountCreationView(generic.CreateView):
    model = CustomUser
    form_class =  CustomUserCreationForm
    template_name = 'accounts/accounts_create.html'
    success_url = reverse_lazy('accounts:login')  # ←ここをログイン画面のURLにする！

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(**self.get_form_kwargs())  # フォームを渡す
        return context
    
# class CustomAccountCreationView(generic.CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        print("フォームが正常に処理され、データベースに保存されました")  # デバッグ用
        return response

    def form_invalid(self, form):
        print("フォームが無効です:", form.errors)  # デバッグ用
        return super().form_invalid(form)

class Login(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm  # これ追加！
    success_url = reverse_lazy('diary:comment_create')

class Logout(LogoutView):
    success_url = reverse_lazy('accounts:login')

