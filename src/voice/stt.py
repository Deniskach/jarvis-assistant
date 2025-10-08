import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Настройка параметров микрофона
        self.recognizer.pause_threshold = self.config['voice']['pause_threshold']
        self.recognizer.energy_threshold = self.config['voice']['energy_threshold']
        
    def recognize(self):
        """Распознает речь из микрофона"""
        try:
            with self.microphone as source:
                print("Слушаю...")
                audio = self.recognizer.listen(source)
                
            text = self.recognizer.recognize_google(
                audio, 
                language=self.config['assistant']['language']
            )
            print(f"Распознано: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")
            return None