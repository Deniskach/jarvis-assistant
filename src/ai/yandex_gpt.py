"""
Клиент для Yandex GPT API
"""
import os
import requests
import json
from dotenv import load_dotenv

class YandexGPTClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('YANDEX_API_KEY')
        self.folder_id = os.getenv('YANDEX_FOLDER_ID')
        self.is_available = False
        
        if self.api_key and self.folder_id:
            self.is_available = True
            print("✅ Yandex GPT клиент инициализирован")
        else:
            print("⚠️  YANDEX_API_KEY или YANDEX_FOLDER_ID не найдены в .env")
    
    def chat(self, message, context=""):
        """Отправляет сообщение в Yandex GPT и получает ответ"""
        if not self.is_available:
            return "Yandex GPT не настроен. Добавьте YANDEX_API_KEY и YANDEX_FOLDER_ID в .env файл"
        
        try:
            # Формируем промпт в стиле Джарвиса
            system_prompt = """Ты - Джарвис, умный голосовой ассистент из вселенной Железного человека. 
Твой характер: профессиональный, немного саркастичный, очень умный и полезный.
Отвечай кратко и по делу, как настоящий ИИ-помощник.
Если вопрос не требует длинного ответа - отвечай кратко."""

            if context:
                system_prompt += f"\nКонтекст: {context}"

            # Подготовка запроса к Yandex GPT
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {
                "Authorization": f"Api-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.7,
                    "maxTokens": 150
                },
                "messages": [
                    {
                        "role": "system",
                        "text": system_prompt
                    },
                    {
                        "role": "user", 
                        "text": message
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['result']['alternatives'][0]['message']['text']
            
        except requests.exceptions.RequestException as e:
            return f"Ошибка сети при обращении к Yandex GPT: {e}"
        except Exception as e:
            return f"Ошибка Yandex GPT: {e}"
    
    def is_configured(self):
        """Проверяет, настроен ли Yandex GPT"""
        return self.is_available