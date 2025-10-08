import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔍 Проверяем установку Vosk...")

try:
    # Проверяем импорт Vosk
    from vosk import Model, KaldiRecognizer
    print("✅ Vosk импортируется успешно")
    
    # Проверяем наличие модели
    model_path = "models/vosk-model-small-ru-0.22"
    if os.path.exists(model_path):
        print(f"✅ Модель найдена в: {model_path}")
        
        # Пробуем загрузить модель
        print("🔄 Пробуем загрузить модель...")
        model = Model(model_path)
        print("✅ Модель загружена успешно!")
        
        # Пробуем создать распознаватель
        recognizer = KaldiRecognizer(model, 16000)
        print("✅ Распознаватель создан успешно!")
        
    else:
        print(f"❌ Модель не найдена в: {model_path}")
        print("💡 Запустите test_vosk.py для автоматической загрузки")
        
except ImportError as e:
    print(f"❌ Ошибка импорта Vosk: {e}")
    print("💡 Установите: pip install vosk")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Проверяем PyAudio...")
try:
    import pyaudio
    p = pyaudio.PyAudio()
    print("✅ PyAudio работает")
    p.terminate()
except Exception as e:
    print(f"❌ Ошибка PyAudio: {e}")