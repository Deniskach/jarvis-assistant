import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Тестируем Джарвиса...")

try:
    from src.voice.stt import SpeechRecognizer
    from src.voice.tts import SpeechSynthesizer
    print("✅ Все модули загружены успешно!")
    
    # Тестируем TTS (синтез речи)
    print("🔊 Тестируем голос...")
    tts = SpeechSynthesizer()
    tts.speak("Привет! Я Джарвис. Микрофон работает!")
    
    # Тестируем STT (распознавание речи)
    print("🎤 Тестируем микрофон...")
    stt = SpeechRecognizer()
    
    print("\n🎯 Говорите команды в микрофон!")
    print("Доступные команды: 'привет', 'время', 'дата', 'стоп'")
    print("Для выхода скажите 'стоп' или нажмите Ctrl+C\n")
    
    while True:
        text = stt.recognize()
        if text:
            if 'привет' in text.lower():
                tts.speak("Привет! Рад вас слышать!")
            elif 'время' in text.lower():
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                tts.speak(f"Сейчас {current_time}")
            elif 'дата' in text.lower():
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                tts.speak(f"Сегодня {current_date}")
            elif any(word in text.lower() for word in ['стоп', 'выход', 'stop']):
                tts.speak("До свидания! Выключаюсь.")
                break
            else:
                tts.speak("Не понял команду. Попробуйте еще раз.")
                
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("📦 Проверьте установленные пакеты:")
    os.system("pip list")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()