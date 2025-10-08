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
        self.engine = None
        self.voice_settings = {
            'rate': 180,        # Скорость речи (слов в минуту)
            'volume': 0.9,      # Громкость (0.0 - 1.0)
            'voice_id': None,   # ID голоса (автовыбор русского)
            'pitch': 50         # Высота тона (не везде поддерживается)
        }
        
        if self.has_tts:
            try:
                self.engine = pyttsx3.init()
                self.setup_voice()
                print("✅ Синтезатор речи инициализирован")
                
            except Exception as e:
                print(f"❌ Ошибка инициализации TTS: {e}")
                self.has_tts = False
        else:
            print("⚠️  TTS недоступен")

    def setup_voice(self):
        """Настраивает голос и параметры речи"""
        if not self.engine:
            return
            
        # Получаем список доступных голосов
        voices = self.engine.getProperty('voices')
        
        # Ищем русский голос
        russian_voices = []
        english_voices = []
        
        for voice in voices:
            if 'russian' in voice.name.lower() or 'russian' in voice.id.lower():
                russian_voices.append(voice)
            elif 'english' in voice.name.lower() or 'english' in voice.id.lower():
                english_voices.append(voice)
        
        # Выбираем голос по приоритету: русский → английский → первый доступный
        if russian_voices:
            selected_voice = russian_voices[0]
            print(f"✅ Найден русский голос: {selected_voice.name}")
        elif english_voices:
            selected_voice = english_voices[0] 
            print(f"⚠️  Русский голос не найден, используется английский: {selected_voice.name}")
        else:
            selected_voice = voices[0] if voices else None
            print(f"⚠️  Используется голос по умолчанию: {selected_voice.name if selected_voice else 'Не найден'}")
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice.id)
            self.voice_settings['voice_id'] = selected_voice.id
        
        # Применяем настройки
        self.engine.setProperty('rate', self.voice_settings['rate'])
        self.engine.setProperty('volume', self.voice_settings['volume'])

    
    def change_voice_speed(self, speed):
        """Изменяет скорость речи"""
        if not self.engine:
            return "Синтезатор речи не инициализирован"
        
        # Ограничиваем диапазон скорости
        speed = max(50, min(300, speed))  # 50-300 слов в минуту
        self.voice_settings['rate'] = speed
        self.engine.setProperty('rate', speed)
        return f"Скорость речи установлена на {speed}"
    

    def change_volume(self, volume):
        """Изменяет громкость"""
        if not self.engine:
            return "Синтезатор речи не инициализирован"
        
        # Ограничиваем диапазон громкости
        volume = max(0.1, min(1.0, volume))  # 0.1-1.0
        self.voice_settings['volume'] = volume
        self.engine.setProperty('volume', volume)
        return f"Громкость установлена на {int(volume * 100)}%"
    

    def list_available_voices(self):
        """Показывает список доступных голосов"""
        if not self.engine:
            return "Синтезатор речи не инициализирован"
        
        voices = self.engine.getProperty('voices')
        result = "Доступные голоса:\n"
        
        for i, voice in enumerate(voices):
            language = "русский" if 'russian' in voice.name.lower() else "английский" if 'english' in voice.name.lower() else "другой"
            current = " (текущий)" if voice.id == self.voice_settings['voice_id'] else ""
            result += f"{i+1}. {voice.name} ({language}){current}\n"
        
        return result
    

    def set_voice(self, voice_index):
        """Устанавливает голос по индексу"""
        if not self.engine:
            return "Синтезатор речи не инициализирован"
        
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            self.voice_settings['voice_id'] = voices[voice_index].id
            return f"Голос изменен на: {voices[voice_index].name}"
        else:
            return f"Голос с индексом {voice_index} не найден"
        

    def get_voice_settings(self):
        """Возвращает текущие настройки голоса"""
        return f"""
Текущие настройки голоса:
• Скорость: {self.voice_settings['rate']} слов/мин
• Громкость: {int(self.voice_settings['volume'] * 100)}%
• Голос: {self.get_current_voice_name()}
"""
    

    def get_current_voice_name(self):
        """Возвращает название текущего голоса"""
        if not self.engine or not self.voice_settings['voice_id']:
            return "Неизвестно"
        
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.id == self.voice_settings['voice_id']:
                return voice.name
        return "Неизвестно"

    
    def speak(self, text):
        """Произносит текст"""
        print(f"🤖 Jarvis: {text}")
        
        if self.has_tts:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"❌ Ошибка воспроизведения: {e}")