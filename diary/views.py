from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
import datetime

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'diary/comment_create.html'
    success_url = reverse_lazy('diary:comment_list')  # 登録後に表示したいページのURL名

    def form_valid(self, form):
        form.instance.user = self.request.user  # ここでログインユーザーをセット！
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.model()  # 空の Comment オブジェクトを渡す
        return context

class CommentListView(ListView):
    model = Comment
    template_name = 'diary/comment_list.html'
    context_object_name = 'object_list'  # テンプレートで使いやすくするための変数名

    def get_queryset(self):
        print(self.request.user)  # ログイン中のユーザーをコンソールに表示
        # ログイン中のユーザーのコメントだけを取得
        return Comment.objects.filter(user=self.request.user)

