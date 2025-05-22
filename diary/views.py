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
    success_url = reverse_lazy('diary:diary_list')  # 登録後に表示したいページのURL名

    def form_valid(self, form):
        # 日記にユーザーを紐付け
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # 感情の状態を文字列としてまとめる（Trueのものだけ取得）
        mood_labels = {
            "mood_happy": "楽しい",
            "mood_sad": "悲しい",
            "mood_angry": "怒っている",
            "mood_anxious": "不安",
            "mood_calm": "落ち着いている",
            "mood_exhausted": "疲れている"
        }

        selected_moods = [
            label for field, label in mood_labels.items()
            if getattr(form.instance, field)
        ]

        mood_str = "、".join(selected_moods) if selected_moods else "未選択"
        username = self.request.user.username if hasattr(self.request.user, 'username') else 'ユーザー'


        # geminiで応援メッセージ生成
        encouragement = generate_encouragement_message(
            form.instance.text,
            self.request.user.personality or "思いやりがあり、穏やかな性格",
            self.request.user.tone or "優しく丁寧な口調",
            username = username,
            mood=mood_str,
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
        self.order = self.request.GET.get('order', 'new')
        queryset = Diary.objects.filter(user=self.request.user)
        return queryset.order_by('-date' if self.order == 'new' else 'date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order  # ← これをテンプレートに渡す
        return context
        
    """    
    def get_queryset(self):
        print(self.request.user)  # ログイン中のユーザーをコンソールに表示
        # ログイン中のユーザーのコメントだけを取得
        return Diary.objects.filter(user=self.request.user).order_by('-date')
    """



class EncouragementView(LoginRequiredMixin, View):
    def get(self, request):
        latest_diary = Diary.objects.filter(user=request.user).order_by('-date').first()

        if latest_diary:
            personality = getattr(request.user, 'personality')
            tone = getattr(request.user, 'tone')
            username = getattr(request.user, 'username')

            mood_labels = {
                "mood_happy": "楽しい",
                "mood_sad": "悲しい",
                "mood_angry": "怒っている",
                "mood_anxious": "不安",
                "mood_calm": "落ち着いている",
                "mood_exhausted": "疲れている"
            }

            selected_moods = [
                label for field, label in mood_labels.items()
                if getattr(latest_diary, field)
            ]
            mood_str = "、".join(selected_moods) if selected_moods else "未選択"

            encouragement = generate_encouragement_message(
                latest_diary.text,
                personality,
                tone,
                username,
                mood_str
            )
        else:
            encouragement = "まだ日記がありません。"

        return render(request, 'diary/encouragement.html', {
            'diary': latest_diary,
            'encouragement': encouragement,
        })


from django.shortcuts import render

def landing_page(request):
    return render(request, 'diary/LP02.html')
