"""
Модуль для управления системными функциями компьютера
"""
import os
import platform
import subprocess
import psutil
import pyautogui

class SystemController:
    def __init__(self):
        self.os_type = platform.system()
        print(f"✅ SystemController инициализирован для {self.os_type}")
    
    def open_program(self, program_name):
        """Открывает программы по имени"""
        programs = {
            'браузер': 'chrome',
            'chrome': 'chrome',
            'блокнот': 'notepad',
            'калькулятор': 'calc',
            'проводник': 'explorer',
            'word': 'winword',
            'excel': 'excel',
            'панель управления': 'control',
            'диспетчер задач': 'taskmgr'
        }
        
        program_key = program_name.lower()
        if program_key in programs:
            try:
                subprocess.Popen(programs[program_key], shell=True)
                return f"Открываю {program_name}"
            except Exception as e:
                return f"Не удалось открыть {program_name}: {e}"
        else:
            return f"Не знаю как открыть {program_name}"
    
    def get_system_info(self):
        """Возвращает информацию о системе"""
        try:
            # Информация о памяти
            memory = psutil.virtual_memory()
            memory_used = round(memory.used / (1024**3), 1)  # GB
            memory_total = round(memory.total / (1024**3), 1)  # GB
            
            # Информация о процессоре
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Информация о батарее (для ноутбуков)
            battery = None
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
            
            info = f"""
💻 Информация о системе:
• Память: {memory_used}GB / {memory_total}GB ({memory.percent}%)
• Процессор: {cpu_percent}% загружен
"""
            
            if battery:
                info += f"• Батарея: {battery.percent}%"
                if battery.power_plugged:
                    info += " (заряжается)"
            
            return info.strip()
            
        except Exception as e:
            return f"Не удалось получить информацию о системе: {e}"
    
    def volume_control(self, action):
        """Управление громкостью"""
        try:
            if action == 'громче':
                for _ in range(5):
                    pyautogui.press('volumeup')
                return "Увеличиваю громкость"
            elif action == 'тише':
                for _ in range(5):
                    pyautogui.press('volumedown')
                return "Уменьшаю громкость"
            elif action == 'выключить звук' or action == 'включить звук':
                pyautogui.press('volumemute')
                return "Переключаю звук"
            else:
                return "Не понял команду громкости"
        except Exception as e:
            return f"Ошибка управления громкостью: {e}"
    
    def computer_control(self, action):
        """Управление компьютером"""
        try:
            if action == 'спать':
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "Перевожу компьютер в спящий режим"
            elif action == 'перезагрузка':
                os.system("shutdown /r /t 5")
                return "Перезагружаю компьютер через 5 секунд"
            elif action == 'выключение':
                os.system("shutdown /s /t 5")
                return "Выключаю компьютер через 5 секунд"
            else:
                return "Не понял команду управления"
        except Exception as e:
            return f"Ошибка управления компьютером: {e}"
    
    def take_screenshot(self):
        try:
            # Основной способ: MSS
            import mss
            from datetime import datetime
            import os

            pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")

            with mss.mss() as sct:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                full_path = os.path.join(pictures_dir, filename)
                sct.shot(output=full_path)
                return "Скриншот сохранен"
            
        except ImportError:
            try:
                # Резервный способ: pyscreeze (если установлен)
                import pyscreeze
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                screenshot = pyscreeze.screenshot()
                screenshot.save(filename)
                return "Скриншот сохранен"
            except Exception:
                return "Для скриншотов установите: pip install mss"
        except Exception as e:
            return f"Ошибка создания скриншота: {e}"