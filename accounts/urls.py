from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'
urlpatterns = [
    #path('accounts_create/', views.AccountCreateView.as_view(), name='accounts_create'),
    #path('accounts_create_with_form/', views.AccountCreateViewUsingMyForm.as_view(), name = 'accounts_create_with_form'),
    path('accounts/accounts_create/', views.CustomAccountCreationView.as_view(), name='accounts_create'),
    path('login/', views.Login.as_view(template_name='accounts/login.html'), name = 'login'),
    path('logout/',  views.Login.as_view(template_name='accounts/login.html'), name = 'logout'),
    # マイページURL
    path('my_page/', views.mypage_view, name='mypage'),
    # プロフィール画像アップロード用
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
]