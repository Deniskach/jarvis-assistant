import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Тестируем упрощенную версию Джарвиса...")

try:
    # Импортируем УПРОЩЕННЫЕ классы
    from src.voice.stt_simple import SimpleSpeechRecognizer
    from src.voice.tts_simple import SimpleSpeechSynthesizer
    print("✅ Упрощенные модули загружены успешно!")
    
    # Тестируем TTS (синтез речи)
    print("🔊 Тестируем голос...")
    tts = SimpleSpeechSynthesizer()
    tts.speak("Привет! Я Джарвис. Система работает!")
    
    # Тестируем STT (распознавание речи)
    print("🎤 Тестируем распознавание...")
    stt = SimpleSpeechRecognizer()
    
    print("\n" + "="*50)
    print("🎯 Джарвис готов к работе!")
    print("Доступные команды:")
    print("  'привет' - приветствие")
    print("  'время' - текущее время") 
    print("  'дата' - текущая дата")
    print("  'стоп' - выход")
    print("="*50 + "\n")
    
    while True:
        text = stt.recognize()
        if text:
            text_lower = text.lower()
            
            if any(word in text_lower for word in ['привет', 'здравствуй', 'hello']):
                tts.speak("Привет! Рад вас слышать!")
            elif 'время' in text_lower:
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                tts.speak(f"Сейчас {current_time}")
            elif 'дата' in text_lower:
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                tts.speak(f"Сегодня {current_date}")
            elif any(word in text_lower for word in ['стоп', 'выход', 'stop', 'exit']):
                tts.speak("До свидания! Выключаюсь.")
                break
            else:
                tts.speak("Не понял команду. Попробуйте еще раз.")
                
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("📋 Проверьте наличие файлов:")
    print("   - src/voice/stt_simple.py")
    print("   - src/voice/tts_simple.py")
    
    # Проверим структуру файлов
    print("\n📁 Содержимое папки src/voice/:")
    try:
        voice_dir = os.path.join(current_dir, 'src', 'voice')
        if os.path.exists(voice_dir):
            for file in os.listdir(voice_dir):
                print(f"   - {file}")
        else:
            print("   Папка src/voice/ не существует!")
    except Exception as dir_error:
        print(f"   Ошибка проверки директории: {dir_error}")
        
except Exception as e:
    print(f"❌ Общая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("👋 Программа завершена.")