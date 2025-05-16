from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('diary_create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('diary_list/', views.DiaryListView.as_view(), name='diary_list'),
]
