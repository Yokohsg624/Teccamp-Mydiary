from django import forms
from .models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title','text', 'mood_happy','mood_sad','mood_angry','mood_anxious','mood_calm','mood_exhausted','image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'タイトルを入力してください'}),
            'text': forms.Textarea(attrs={'placeholder': '今日の出来事を入力してください'}),
            'image': forms.ClearableFileInput(),
        }
        
        labels = {
            'title': 'タイトル：',
            'text': '今日の出来事：',
            'mood_happy': '楽しい',
            'mood_sad': '悲しい',
            'mood_angry': '怒っている',
            'mood_anxious': '不安',
            'mood_calm': '落ち着いている',
            'mood_exhausted': '疲れている',
            'image': '画像：',
        }
