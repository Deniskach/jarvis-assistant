import pyttsx3

class SpeechSynthesizer:
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        
        # Базовая настройка голоса
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)  # Скорость речи
    
    def speak(self, text):
        """Произносит текст"""
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()