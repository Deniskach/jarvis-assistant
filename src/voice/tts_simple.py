"""
Упрощенная версия синтеза речи
"""
try:
    import pyttsx3
    print("✅ pyttsx3 загружен")
    HAS_TTS = True
except ImportError as e:
    print(f"❌ Ошибка загрузки pyttsx3: {e}")
    HAS_TTS = False

class SimpleSpeechSynthesizer:
    def __init__(self):
        self.has_tts = HAS_TTS
        
        if self.has_tts:
            try:
                self.engine = pyttsx3.init()
                
                # Базовая настройка голоса
                voices = self.engine.getProperty('voices')
                if voices:
                    # Ищем русский голос
                    for voice in voices:
                        if 'russian' in voice.name.lower() or 'russian' in voice.id.lower():
                            self.engine.setProperty('voice', voice.id)
                            print(f"✅ Найден русский голос: {voice.name}")
                            break
                    else:
                        self.engine.setProperty('voice', voices[0].id)
                        print(f"✅ Используем голос по умолчанию: {voices[0].name}")
                
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.8)
                print("✅ Синтезатор речи инициализирован")
                
            except Exception as e:
                print(f"❌ Ошибка инициализации TTS: {e}")
                self.has_tts = False
        else:
            print("⚠️  TTS недоступен")
    
    def speak(self, text):
        """Произносит текст"""
        print(f"🤖 Jarvis: {text}")
        
        if self.has_tts:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"❌ Ошибка воспроизведения: {e}")