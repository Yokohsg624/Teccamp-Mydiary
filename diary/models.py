from django.db import models

# 日記の入力モデル
class Diary(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='ユーザー', null=True)
    title = models.CharField('タイトル', max_length=100)
    date = models.DateField('投稿日時', auto_now_add=True)
    text = models.TextField('今日の出来事', max_length=1000)

    #気分を選択するためのフィールド
    mood_happy  = models.BooleanField('楽しい', default=False)
    mood_sad  = models.BooleanField('悲しい', default=False)
    mood_angry  = models.BooleanField('怒っている', default=False)
    mood_anxious  = models.BooleanField('不安', default=False)
    mood_calm  = models.BooleanField('落ち着いている', default=False)
    mood_exhausted  = models.BooleanField('疲れている', default=False)

    #あれば画像を追加するためのフィールド
    image = models.ImageField('画像', upload_to='diary/images/', blank=True, null=True)

    def __str__(self):
        return f"Diary by {self.user.username if self.user else 'Unknown'}"
    
    class Meta:
        db_table = 'diary'  # ここでテーブル名を指定！