"""
Упрощенная версия распознавания речи
"""
import sys
import os

try:
    import speech_recognition as sr
    print("✅ speech_recognition загружен")
    HAS_SPEECH_RECOGNITION = True
except ImportError as e:
    print(f"❌ Ошибка загрузки speech_recognition: {e}")
    HAS_SPEECH_RECOGNITION = False

class SimpleSpeechRecognizer:
    def __init__(self):
        self.has_microphone = False
        
        if HAS_SPEECH_RECOGNITION:
            try:
                self.recognizer = sr.Recognizer()
                # Пробуем найти рабочий микрофон
                try:
                    self.microphone = sr.Microphone()
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source)
                    self.has_microphone = True
                    print("✅ Микрофон инициализирован")
                except Exception as e:
                    print(f"⚠️  Микрофон недоступен: {e}")
                    self.has_microphone = False
                    
            except Exception as e:
                print(f"❌ Ошибка инициализации распознавателя: {e}")
                self.has_microphone = False
        else:
            print("⚠️  Режим без распознавания речи")
    
    def recognize(self):
        """Распознает речь или получает текст из консоли"""
        if not self.has_microphone:
            # Режим без микрофона - ввод с клавиатуры
            try:
                text = input("🎤 Введите команду текстом: ")
                return text.lower()
            except (KeyboardInterrupt, EOFError):
                return "стоп"
        
        try:
            with self.microphone as source:
                print("🎤 Говорите сейчас...")
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=6)
                
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            print(f"📝 Распознано: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("❌ Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка сервиса распознавания: {e}")
            return None
        except sr.WaitTimeoutError:
            print("⏰ Таймаут ожидания речи")
            return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None