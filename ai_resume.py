import os
import requests
from dotenv import load_dotenv
import whisper 

load_dotenv()

# Comet API (для анализа текста)
DOC_COMET_API_KEY = os.getenv("DOC_COMET_API_KEY")
DOC_COMET_API_URL = os.getenv("DOC_COMET_API_URL")

HEADERS = {
    "Authorization": f"Bearer {DOC_COMET_API_KEY}",
    "Content-Type": "application/json",
}

# 🔍 Анализ текстового резюме через Comet
def analyze_text_resume(text: str) -> str:
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Ты — эксперт по оценке резюме. Оцени текст резюме и дай рекомендации."},
            {"role": "user", "content": text},
        ],
        "temperature": 0.3,
        "max_tokens": 1500,
    }

    response = requests.post(DOC_COMET_API_URL, headers=HEADERS, json=data)
    if response.status_code != 200:
        return f"Ошибка: {response.status_code}"

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка обработки ответа: {e}"

# 🎥 Анализ видео-резюме через Whisper + Comet
def analyze_video_resume(video_path: str) -> str:
    try:
        model = whisper.load_model("base")  # можно заменить на "small" или "medium"
        result = model.transcribe(video_path)
        transcript_text = result["text"]

        return analyze_text_resume(transcript_text)

    except Exception as e:
        return f"Ошибка обработки видео: {str(e)}"
