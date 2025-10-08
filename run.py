import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Запуск Джарвиса...")

try:
    from src.voice.stt import VoskSpeechRecognizer as SpeechRecognizer
    from src.voice.tts import SimpleSpeechSynthesizer as SpeechSynthesizer
    print("✅ Модули загружены успешно!")
    
    class Jarvis:
        def __init__(self):
            self.stt = SpeechRecognizer()
            self.tts = SpeechSynthesizer()
            
        def process_command(self, text):
            """Обрабатывает команды"""
            text_lower = text.lower()
            
            if any(word in text_lower for word in ['привет', 'здравствуй']):
                self.tts.speak("Привет! Чем могу помочь?")
            elif 'время' in text_lower:
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                self.tts.speak(f"Сейчас {current_time}")
            elif 'дата' in text_lower:
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                self.tts.speak(f"Сегодня {current_date}")
            elif any(word in text_lower for word in ['стоп', 'выход']):
                self.tts.speak("До свидания!")
                return False  # сигнал для выхода
            else:
                self.tts.speak("Не понял команду")
            return True
            
        def run(self):
            """Основной цикл"""
            self.tts.speak("Джарвис запущен. Говорите команды.")
            print("\n🎯 Доступные команды: привет, время, дата, стоп")
            
            while True:
                text = self.stt.recognize()
                if text and not self.process_command(text):
                    break
                    
    # Запуск
    jarvis = Jarvis()
    jarvis.run()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("👋 Завершено.")