"""
Распознавание речи с использованием Vosk (оффлайн)
"""
import os
import json
import pyaudio
import sys

class VoskSpeechRecognizer:
    def __init__(self, model_path=None):
        self.model = None
        self.recognizer = None
        self.audio = None
        
        # Путь к модели
        if model_path is None:
            model_path = "models/vosk-model-small-ru-0.22"
        
        self.model_path = model_path
        self.setup_model()
    
    def setup_model(self):
        """Настраивает модель распознавания"""
        try:
            print(f"🔍 Проверяем модель в: {os.path.abspath(self.model_path)}")
            
            if not os.path.exists(self.model_path):
                print(f"📥 Модель не найдена в {self.model_path}")
                print("🔄 Скачиваем небольшую русскую модель...")
                self.download_model()
            
            print("🔄 Загружаем модель Vosk...")
            from vosk import Model, KaldiRecognizer
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
            
            # Инициализируем PyAudio после успешной загрузки модели
            self.audio = pyaudio.PyAudio()
            
            print("✅ Модель Vosk загружена и готова к работе")
            
        except ImportError as e:
            print(f"❌ Ошибка импорта Vosk: {e}")
            print("💡 Убедитесь, что установлен vosk: pip install vosk")
        except Exception as e:
            print(f"❌ Ошибка загрузки модели Vosk: {e}")
            import traceback
            traceback.print_exc()
    
    def download_model(self):
        """Скачивает модель Vosk для русского языка"""
        try:
            import urllib.request
            import zipfile
            
            model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
            zip_path = "models/vosk-model-small-ru-0.22.zip"
            
            # Создаем папку models если нет
            os.makedirs("models", exist_ok=True)
            
            print(f"📥 Скачиваем модель из {model_url}...")
            urllib.request.urlretrieve(model_url, zip_path)
            
            print("📦 Распаковываем модель...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("models/")
            
            # Удаляем zip файл
            os.remove(zip_path)
            print("✅ Модель успешно скачана и распакована")
            
        except Exception as e:
            print(f"❌ Ошибка скачивания модели: {e}")
            print("💡 Скачайте вручную: https://alphacephei.com/vosk/models")
            print("💡 И распакуйте в папку models/")
    
    def recognize(self):
        """Распознает речь из микрофона"""
        if self.recognizer is None or self.audio is None:
            print("❌ Модель или аудио не инициализированы")
            print("💡 Переходим в текстовый режим")
            return self.fallback_input()
        
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000
            )
            
            print("🎤 Говорите сейчас... (для остановки нажмите Ctrl+C)")
            print("⏳ Слушаю...", end='', flush=True)
            
            stream.start_stream()
            
            try:
                while True:
                    data = stream.read(4000, exception_on_overflow=False)
                    
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                        if text:
                            print(f"\n📝 Распознано: {text}")
                            stream.stop_stream()
                            stream.close()
                            return text.lower()
                    else:
                        # Частичный результат
                        partial_result = json.loads(self.recognizer.PartialResult())
                        partial_text = partial_result.get('partial', '')
                        if partial_text:
                            print(f"\r⏳ Слушаю: {partial_text}...", end='', flush=True)
                            
            except KeyboardInterrupt:
                print("\n⏹️  Остановлено пользователем")
                stream.stop_stream()
                stream.close()
                return "стоп"
                
        except Exception as e:
            print(f"\n❌ Ошибка распознавания: {e}")
            return self.fallback_input()
    
    def fallback_input(self):
        """Резервный текстовый ввод"""
        try:
            text = input("\n🎤 Введите команду текстом: ")
            return text.lower()
        except (KeyboardInterrupt, EOFError):
            return "стоп"
    
    def __del__(self):
        if self.audio:
            self.audio.terminate()