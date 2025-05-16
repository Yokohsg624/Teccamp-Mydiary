from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model # 追加
from django.contrib.auth.mixins import UserPassesTestMixin # 追加
from django.contrib.auth import get_user_model # 追加
from django.contrib.auth.mixins import UserPassesTestMixin # 追加

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
    success_url = reverse_lazy('diary:diary_create')

class Logout(LogoutView):
    success_url = reverse_lazy('accounts:login')

User = get_user_model()  # ユーザーモデルを取得

'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == int(self.kwargs['pk'])  # ここを修正


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'accounts/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される