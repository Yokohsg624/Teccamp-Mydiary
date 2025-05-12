from django.contrib import admin
from .models import Comment

# CommentモデルをAdminサイトに登録
admin.site.register(Comment)