from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Diary
from .forms import DiaryForm
#import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_create.html'
    success_url = reverse_lazy('diary:diary_list')  # 登録後に表示したいページのURL名

    def form_valid(self, form):
        form.instance.user = self.request.user  # ここでログインユーザーをセット！
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diary'] = self.model()  # 空の Diary オブジェクトを渡す
        return context

class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'object_list'  # テンプレートで使いやすくするための変数名

    def get_queryset(self):
        print(self.request.user)  # ログイン中のユーザーをコンソールに表示
        # ログイン中のユーザーのコメントだけを取得
        return Diary.objects.filter(user=self.request.user)

