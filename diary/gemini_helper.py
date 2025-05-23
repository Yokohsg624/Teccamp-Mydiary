import os
import google.generativeai as genai
from django.conf import settings # Djangoのプロジェクトであれば必要

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEYが設定されていません。") # APIキーがない場合のエラー処理

genai.configure(api_key=api_key)
#print(f"APIキーが設定されました: {api_key[:5]}...") # APIキーの一部を表示（デバッグ用、本番では削除推奨）

def generate_encouragement_message(diary_text, personality, tone, username, mood):
    try:
        # 利用可能なモデルを選択 (例: gemini-1.5-flash-latest)
        # モデル名は適宜変更してください
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        
        prompt = f"""
        あなたはユーザーのパートナーであり、ユーザーが書いた日記を読んでフィードバックすることで、癒しを与えます。
        以下の条件をもとに、メッセージ（4〜10行程度）を生成してください。

        - あなたの性格：{personality}
        - あなたの口調：{tone}
        - ユーザーの名前：{username}
        - ユーザーの今日の気分：{mood}
        - ユーザーの日記内容：
        {diary_text}
        """
        
        response = model.generate_content(prompt)
        
        # レスポンスの構造によっては、 .text 以外の場合もあります。
        # print(response) # デバッグ用にレスポンス全体を確認
        if response.parts:
            return response.text
        else:
            # 候補がない場合や、他の理由でテキストが直接 .text にない場合を考慮
            # 必要に応じて response.candidates[0].content.parts[0].text のようにアクセス
            return "geminiからのメッセージを生成できませんでした。(レスポンス形式エラー)"

    except Exception as e:
        print(f"Gemini API エラー: {e}")
        return "geminiからのメッセージを生成できませんでした。"
