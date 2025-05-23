from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'
urlpatterns = [
    #path('accounts_create/', views.AccountCreateView.as_view(), name='accounts_create'),
    #path('accounts_create_with_form/', views.AccountCreateViewUsingMyForm.as_view(), name = 'accounts_create_with_form'),
    path('accounts/accounts_create/', views.CustomAccountCreationView.as_view(), name='accounts_create'),
    path('login/', views.Login.as_view(template_name='accounts/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    # マイページURL
    path('my_page/', views.mypage_view, name='mypage'),
]