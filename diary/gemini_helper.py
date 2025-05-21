import os
import google.generativeai as genai
from django.conf import settings # Djangoのプロジェクトであれば必要

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEYが設定されていません。") # APIキーがない場合のエラー処理

genai.configure(api_key=api_key)
#print(f"APIキーが設定されました: {api_key[:5]}...") # APIキーの一部を表示（デバッグ用、本番では削除推奨）

def generate_encouragement_message(diary_text, personality, tone):
    try:
        # 利用可能なモデルを選択 (例: gemini-1.5-flash-latest)
        # モデル名は適宜変更してください
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        
        prompt = f"""
                    あなたはユーザーのパートナーであり、言葉でユーザーを癒します。\n
                    あなたの性格は「{personality}」です\n
                    あなたの口調は「{tone}」です\n
                    この日記の内容に対して、4~10行以内で、優しくてポジティブな励ましの言葉を日本語で送ってください。\n
                    「{diary_text}」
                    """
        
        response = model.generate_content(prompt)
        
        # レスポンスの構造によっては、 .text 以外の場合もあります。
        # print(response) # デバッグ用にレスポンス全体を確認
        if response.parts:
            return response.text
        else:
            # 候補がない場合や、他の理由でテキストが直接 .text にない場合を考慮
            # 必要に応じて response.candidates[0].content.parts[0].text のようにアクセス
            print(f"Gemini APIからのレスポンスに予期したテキストが含まれていません: {response}")
            return "geminiからのメッセージを生成できませんでした。(レスポンス形式エラー)"

    except Exception as e:
        print(f"Gemini API エラー: {e}")
        return "geminiからのメッセージを生成できませんでした。"
