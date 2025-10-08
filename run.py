import sys
import os

# Добавляем текущую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🚀 Запуск Джарвиса...")

try:
    from src.voice.stt import VoskSpeechRecognizer as SpeechRecognizer
    from src.voice.tts import SimpleSpeechSynthesizer as SpeechSynthesizer
    from src.system.system_controller import SystemController
    print("✅ Модули загружены успешно!")
    
    class Jarvis:
        def __init__(self):
            self.stt = SpeechRecognizer()
            self.tts = SpeechSynthesizer()
            self.system = SystemController()
            
        def process_command(self, text):
            """Обрабатывает команды"""
            text_lower = text.lower()
            
            # Базовые команды
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
            
            # Системные команды
            elif any(word in text_lower for word in ['открой', 'запусти']):
                program = text_lower.replace('открой', '').replace('запусти', '').strip()
                response = self.system.open_program(program)
                self.tts.speak(response)
            
            elif 'система' in text_lower or 'информация о системе' in text_lower:
                response = self.system.get_system_info()
                self.tts.speak(response)
            
            elif any(word in text_lower for word in ['громче', 'тише', 'выключи звук', 'включи звук']):
                if 'громче' in text_lower:
                    action = 'громче'
                elif 'тише' in text_lower:
                    action = 'тише'
                elif 'выключи звук' in text_lower:
                    action = 'выключить звук'
                else:
                    action = 'включить звук'

                response = self.system.volume_control(action)
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
            
            elif any(word in text_lower for word in ['стоп', 'выход']):
                self.tts.speak("До свидания!")
                return False  # сигнал для выхода
            
            else:
                self.tts.speak("Не понял команду")
            return True
            
        def run(self):
            """Основной цикл"""
            self.tts.speak("Джарвис запущен. Говорите команды.")
            print("\n" + "="*60)
            print("🎯 ДОСТУПНЫЕ КОМАНДЫ:")
            print("• Базовые: привет, время, дата")
            print("• Система: открой браузер, открой блокнот")
            print("• Громкость: громче, тише, выключи звук, включи звук") 
            print("• Управление: спать, перезагрузка, выключение")
            print("• Другое: скриншот, информация о системе")
            print("• Выход: стоп, выход")
            print("="*60 + "\n")
            
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