from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('comment_create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment_list/', views.CommentListView.as_view(), name='comment_list'),
]
