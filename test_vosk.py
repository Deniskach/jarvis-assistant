import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Тестируем Vosk распознавание речи...")

try:
    from src.voice.stt_vosk import VoskSpeechRecognizer
    from src.voice.tts_simple import SimpleSpeechSynthesizer
    print("✅ Модули загружены успешно!")
    
    # Тестируем TTS
    print("🔊 Тестируем голос...")
    tts = SimpleSpeechSynthesizer()
    tts.speak("Привет! Я Джарвис с оффлайн распознаванием речи!")
    
    # Тестируем Vosk распознавание
    print("🎤 Инициализируем Vosk...")
    stt = VoskSpeechRecognizer()
    
    print("\n" + "="*50)
    print("🎯 Джарвис с Vosk готов к работе!")
    print("Говорите команды в микрофон:")
    print("  'привет' - приветствие")
    print("  'время' - текущее время") 
    print("  'дата' - текущая дата")
    print("  Для выхода нажмите Ctrl+C")
    print("="*50 + "\n")
    
    while True:
        text = stt.recognize()
        if text:
            if any(word in text for word in ['привет', 'здравствуй', 'hello']):
                tts.speak("Привет! Рад вас слышать!")
            elif 'время' in text:
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                tts.speak(f"Сейчас {current_time}")
            elif 'дата' in text:
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                tts.speak(f"Сегодня {current_date}")
            elif any(word in text for word in ['стоп', 'выход', 'stop', 'exit']):
                tts.speak("До свидания! Выключаюсь.")
                break
            else:
                tts.speak("Не понял команду. Попробуйте еще раз.")
                
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Общая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("👋 Программа завершена.")