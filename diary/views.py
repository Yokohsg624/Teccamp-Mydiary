from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Diary
from .forms import DiaryForm
#import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from .gemini_helper import generate_encouragement_message  # ファイル名に合わせてね！
from django.shortcuts import redirect
from django.views import View
#from django.shortcuts import render, get_object_or_404
from diary.gemini_helper import generate_encouragement_message
from django.shortcuts import render

class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_create.html'
    success_url = reverse_lazy('diary:encouragement')  # 登録後に表示したいページのURL名

    def form_valid(self, form):
        # 日記にユーザーを紐付け
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # geminiで応援メッセージ生成
        encouragement = generate_encouragement_message(
            form.instance.text,
            self.request.user.personality or "思いやりがあり、穏やかな性格",
            self.request.user.tone or "優しく丁寧な口調"
        )

        # 応援メッセージをモデルにセットして再度保存
        form.instance.encouragement_message = encouragement
        form.instance.save(update_fields=['encouragement_message'])
        
        return response

class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'object_list'  # テンプレートで使いやすくするための変数名

    def get_queryset(self):
        print(self.request.user)  # ログイン中のユーザーをコンソールに表示
        # ログイン中のユーザーのコメントだけを取得
        return Diary.objects.filter(user=self.request.user).order_by('-date')

class EncouragementView(LoginRequiredMixin, View):
    def get(self, request):

        # ユーザーの最新の日記を取得（投稿日時で降順）
        latest_diary = Diary.objects.filter(user=request.user).order_by('-date').first()
        #print("送る日記テキスト:", latest_diary.text)

        if latest_diary:
            # 👇 personality と tone をリクエストユーザーから取得
            personality = request.user.personality or "思いやりがあり、穏やかな性格"
            tone = request.user.tone or "優しく丁寧な口調"

            # 👇 3つの引数を渡して関数を正しく呼び出す
            encouragement = generate_encouragement_message(
                latest_diary.text, personality, tone
            )
        else:
            encouragement = "まだ日記がありません。"

        return render(request, 'diary/encouragement.html', {
            'diary': latest_diary,
            'encouragement': encouragement,
        })



