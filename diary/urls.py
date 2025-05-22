from django.urls import path
from . import views
from .views import EncouragementView

app_name = 'diary'
urlpatterns = [
    path('', views.landing_page, name='landing'),  # トップページに設定
    path('diary_create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('diary_list/', views.DiaryListView.as_view(), name='diary_list'),
    path('encouragement/', EncouragementView.as_view(), name='encouragement'),
]
