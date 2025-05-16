from django.contrib import admin
from .models import Diary

# DiaryモデルをAdminサイトに登録
admin.site.register(Diary)