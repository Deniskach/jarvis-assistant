import sys
import os
import re

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Запуск Джарвиса...")

try:
    from src.voice.stt import VoskSpeechRecognizer as SpeechRecognizer
    from src.voice.tts import SimpleSpeechSynthesizer as SpeechSynthesizer
    from src.system.system_controller import SystemController
    from src.ai.yandex_gpt import YandexGPTClient
    from src.ai.ai_manager import AIManager
    print("✅ Модули загружены успешно!")
    
    class Jarvis:
        def __init__(self):
            self.stt = SpeechRecognizer()
            self.tts = SpeechSynthesizer()
            self.system = SystemController()
            self.ai_client = YandexGPTClient()
            self.ai_manager = AIManager()
            self.activation_phrase = "джарвис" 
            self.is_activated = False
        
        def _words_to_number(self, text):
            """Преобразует слова в числа (например: 'восемьдесят' → 80)"""
            number_words = {
                'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10,
                'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать': 14,
                'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18,
                'девятнадцать': 19, 'двадцать': 20, 'тридцать': 30, 'сорок': 40,
                'пятьдесят': 50, 'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80,
                'девяносто': 90, 'сто': 100
            }
            
            # Ищем числа в тексте
            words = text.split()
            for word in words:
                if word in number_words:
                    return number_words[word]
            
            # Пробуем найти составные числа (например: "двадцать пять")
            for i in range(len(words) - 1):
                if words[i] in number_words and words[i+1] in number_words:
                    tens = number_words[words[i]]
                    ones = number_words[words[i+1]]
                    if tens >= 20 and ones < 10:
                        return tens + ones
            
            # Пробуем найти цифры
            numbers = re.findall(r'\d+', text)
            if numbers:
                return int(numbers[0])
            
            return None
        
        def _is_volume_command(self, text):
            """Определяет, является ли текст командой управления громкостью"""
            text_lower = text.lower()
            
            # Явные команды управления громкостью
            volume_commands = [
                'громче', 'тише', 'выключи звук', 'включи звук', 
                'увеличь громкость', 'уменьши громкость',
                'сделай громче', 'сделай тише'
            ]
            
            # Вопросы и разговоры о громкости
            volume_questions = [
                'что тише', 'что громче', 'тише водопад', 'громче самолет',
                'какой тише', 'какой громче', 'мнение о том что тише',
                'считаешь что тише', 'думаешь что тише'
            ]
            
            # Проверяем, это команда или вопрос
            for command in volume_commands:
                if text_lower == command or text_lower.startswith(command + ' '):
                    return True
                    
            for question in volume_questions:
                if question in text_lower:
                    return False
            
            # Если есть слова "тише" или "громче" в начале фразы - вероятно команда
            if text_lower.startswith(('громче', 'тише')):
                return True
                
            # Если это короткая фраза с этими словами - вероятно команда
            if len(text_lower.split()) <= 3 and any(word in text_lower for word in ['громче', 'тише']):
                return True
            
            # Во всех остальных случаях считаем что это не команда
            return False
        
        def process_command(self, text):
            """Обрабатывает команды"""
            text_lower = text.lower()
            
            # ПЕРВОЕ: Проверяем команды громкости с умным определением
            if any(word in text_lower for word in ['громче', 'тише', 'выключи звук', 'включи звук']):
                is_volume_command = self._is_volume_command(text_lower)
                
                if is_volume_command:
                    # Это команда управления громкостью
                    if 'громче' in text_lower:
                        action = 'громче'
                    elif 'тише' in text_lower:
                        action = 'тише'
                    elif 'включи звук' in text_lower:
                        action = 'включить звук'
                    else:
                        action = 'выключить звук'
                    response = self.system.volume_control(action)
                    self.tts.speak(response)
                    return True
                else:
                    # Это вопрос или разговор - отправляем в ИИ
                    if self.ai_client.is_configured():
                        context = self.ai_manager.get_conversation_context()
                        response = self.ai_client.chat(text, context)
                        self.ai_manager.add_to_history(text, response)
                    else:
                        response = "ИИ не настроен"
                    self.tts.speak(response)
                    return True
            
            # ВТОРОЕ: Остальные команды
            # Базовые команды (обрабатываются локально)
            if any(word in text_lower for word in ['привет', 'здравствуй']):
                response = "Привет! Я Джарвис. Чем могу помочь?"
                self.tts.speak(response)
            
            elif 'время' in text_lower:
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                response = f"Сейчас {current_time}"
                self.tts.speak(response)
            
            elif 'дата' in text_lower:
                from datetime import datetime
                current_date = datetime.now().strftime("%d %B %Y")
                response = f"Сегодня {current_date}"
                self.tts.speak(response)
            
            # Системные команды
            elif any(word in text_lower for word in ['открой', 'запусти']):
                program = text_lower.replace('открой', '').replace('запусти', '').strip()
                response = self.system.open_program_advanced(program)
                self.tts.speak(response)
            
            elif 'система' in text_lower or 'информация о системе' in text_lower:
                response = self.system.get_system_info()
                self.tts.speak(response)
            
            elif any(word in text_lower for word in ['спать', 'перезагрузка', 'выключение']):
                if 'спать' in text_lower:
                    action = 'спать'
                elif 'перезагрузка' in text_lower:
                    action = 'перезагрузка'
                else:
                    action = 'выключение'
                response = self.system.computer_control(action)
                self.tts.speak(response)
            
            elif 'скриншот' in text_lower:
                response = self.system.take_screenshot()
                self.tts.speak(response)
            
            # Настройки голоса
            elif 'скорость речи' in text_lower or 'скорость' in text_lower:
                try:
                    if 'быстрее' in text_lower:
                        current_speed = self.tts.voice_settings['rate']
                        new_speed = min(300, current_speed + 50)
                        response = self.tts.change_voice_speed(new_speed)
                        self.tts.speak(response)
                        
                    elif 'медленнее' in text_lower:
                        current_speed = self.tts.voice_settings['rate']
                        new_speed = max(50, current_speed - 50)
                        response = self.tts.change_voice_speed(new_speed)
                        self.tts.speak(response)
                        
                    else:
                        # Преобразуем слова в числа
                        speed_number = self._words_to_number(text_lower)
                        if speed_number is not None:
                            response = self.tts.change_voice_speed(speed_number)
                            self.tts.speak(response)
                        else:
                            self.tts.speak("Скажите 'скорость речи 200' или 'скорость речи быстрее'")
                            
                except Exception as e:
                    self.tts.speak("Ошибка настройки скорости")

            elif 'список голосов' in text_lower:
                response = self.tts.list_available_voices()
                self.tts.speak(response)

            elif 'настройки голоса' in text_lower:
                response = self.tts.get_voice_settings()
                self.tts.speak(response)

            elif 'смени голос' in text_lower or 'измени голос' in text_lower:
                try:
                    numbers = re.findall(r'\d+', text)
                    voice_index = int(numbers[0]) - 1 if numbers else 0
                    response = self.tts.set_voice(voice_index)
                    self.tts.speak(response)
                except:
                    self.tts.speak("Скажите 'смени голос 1', 'смени голос 2' и т.д.")
            
            # Команды ИИ
            elif 'очисти историю' in text_lower or 'забудь всё' in text_lower:
                self.ai_manager.clear_history()
                response = "История разговора очищена"
                self.tts.speak(response)
            
            elif any(word in text_lower for word in ['стоп', 'выход', 'пока']):
                self.tts.speak("До свидания!")
                return False

            # Все остальное отправляем в ИИ
            else:
                if self.ai_manager.should_use_ai(text):
                    if self.ai_client.is_configured():
                        context = self.ai_manager.get_conversation_context()
                        response = self.ai_client.chat(text, context)
                        self.ai_manager.add_to_history(text, response)
                    else:
                        response = "ИИ не настроен. Добавьте API ключи в файл .env"
                    self.tts.speak(response)
                else:
                    self.tts.speak("Не понял команду")
            
            return True
            
        def run(self):
            """Основной цикл"""
            self.tts.speak("Джарвис запущен. Говорите команды.")
            print("\n" + "="*70)
            print("🎯 ДОСТУПНЫЕ КОМАНДЫ:")
            print("• Голос: скорость речи, громкость голоса, список голосов, настройки голоса, смени голос")
            print("• Базовые: привет, время, дата")
            print("• Система: открой браузер, открой блокнот")
            print("• Громкость: громче, тише, выкл/вкл звук") 
            print("• Скриншоты: скриншот")
            print("• Управление: спать, перезагрузка, выключение")
            print("• Информация: информация о системе")
            print("• ИИ: задавайте любые вопросы!")
            print("• Утилиты: очисти историю")
            print("• Выход: стоп, выход")
            print("="*70 + "\n")
            
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