from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
#from django.views.generic import TemplateView
from .forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model # 追加
#from django.contrib.auth.mixins import UserPassesTestMixin # 追加
from django.contrib.auth import get_user_model # 追加
#from django.contrib.auth.mixins import UserPassesTestMixin # 追加
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from .forms import ProfileImageForm
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login

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
    #success_url = reverse_lazy('accounts:login')
    next_page = reverse_lazy('accounts:login')

User = get_user_model()  # ユーザーモデルを取得


@login_required
def mypage_view(request):
    if request.method == 'POST':
        print(request.FILES.keys())  # request.FILESの中身を確認！
        print(request.FILES.keys())  # デバッグ用に送信されたファイルのキーをプリント

        user = request.user  # ログイン中のユーザーを取得
        
        if 'profile_image' in request.FILES:  # ファイルが送信されているかチェック！
            image = request.FILES['profile_image']
            user = request.user  # ログイン中のユーザーを取得
            user.profile_image = image  # 新しい画像を保存！
            user.save()  # モデルのインスタンスを保存！
            return redirect('accounts:mypage')  # マイページを再描画！
        
        # 追加: toneとpersonalityの保存処理
        tone = request.POST.get('tone')
        personality = request.POST.get('personality')

        if tone is not None:
            user.tone = tone
        if personality is not None:
            user.personality = personality

        user.save()
        return redirect('accounts:mypage')

    # GETの場合（マイページのデフォルト表示）
    diary_count = request.user.diary_set.count()
    profile_image_url = request.user.profile_image.url if request.user.profile_image else None

    # 🔽 ここで "None" っていう文字列を空文字にする！
    tone = request.user.tone if request.user.tone != "None" else ""
    personality = request.user.personality if request.user.personality != "None" else ""

    return render(request, 'accounts/my_page.html', {
        'diary_count': diary_count,
        'profile_image_url': profile_image_url,
        'tone': tone,
        'personality': personality,
    })

@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        user = request.user
        user.profile_image = request.FILES['image']
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}) 

