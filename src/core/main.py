import logging
from src.core.config_loader import ConfigLoader
from src.voice.stt import SpeechRecognizer
from src.voice.tts import SpeechSynthesizer

class Jarvis:
    def __init__(self):
        self.config = ConfigLoader().load()
        self.setup_logging()
        self.stt = SpeechRecognizer(self.config)
        self.tts = SpeechSynthesizer(self.config)
        self.is_listening = False
        
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.config['logging']['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("Jarvis")
        
    def listen(self):
        """Слушает и распознает команды"""
        try:
            text = self.stt.recognize()
            if text:
                self.process_command(text)
        except Exception as e:
            self.logger.error(f"Ошибка при распознавании: {e}")
            
    def process_command(self, text):
        """Обрабатывает распознанную команду"""
        self.logger.info(f"Распознана команда: {text}")
        
        # Базовая логика команд
        if any(word in text.lower() for word in ['привет', 'здравствуй']):
            self.tts.speak("Здравствуйте! Чем могу помочь?")
        elif 'время' in text.lower():
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            self.tts.speak(f"Сейчас {current_time}")
        else:
            self.tts.speak("Не понял команду. Повторите, пожалуйста.")
            
    def run(self):
        """Основной цикл работы"""
        self.tts.speak(f"{self.config['assistant']['name']} запущен и готов к работе")
        self.logger.info("Ассистент запущен")
        
        while True:
            self.listen()

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()