"""
Менеджер искусственного интеллекта
"""
class AIManager:
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10  # Максимальное количество сообщений в истории
        
    def should_use_ai(self, text):
        """Определяет, нужно ли использовать ИИ для ответа"""
        text_lower = text.lower()
        
        # Команды которые обрабатываются локально
        local_commands = [
            'привет', 'время', 'дата', 'открой', 'запусти', 'громче', 
            'тише', 'выключи звук', 'скриншот', 'спать', 'перезагрузка',
            'выключение', 'информация о системе', 'стоп', 'выход'
        ]
        
        # Если это явная команда - обрабатываем локально
        for command in local_commands:
            if command in text_lower:
                return False
        
        # Используем ИИ для всего остального
        return True
    
    def add_to_history(self, user_message, ai_response):
        """Добавляет сообщение в историю"""
        self.conversation_history.append({"user": user_message, "ai": ai_response})
        
        # Ограничиваем размер истории
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
    
    def get_conversation_context(self):
        """Возвращает контекст разговора"""
        if not self.conversation_history:
            return ""
        
        context = "Предыдущий разговор:\n"
        for i, exchange in enumerate(self.conversation_history[-3:], 1):  # Последние 3 обмена
            context += f"Пользователь: {exchange['user']}\n"
            context += f"Джарвис: {exchange['ai']}\n"
        
        return context
    
    def clear_history(self):
        """Очищает историю разговора"""
        self.conversation_history = []