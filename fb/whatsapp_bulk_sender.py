import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional
import csv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bulk_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

class WhatsAppBulkSender:
    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.phone_number_id = None
        self.base_url = "https://graph.facebook.com/v23.0"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Лимиты для отправки
        self.messages_per_second = 80  # Максимум 80 сообщений в секунду
        self.pair_rate_limit = 0.17  # 1 сообщение каждые 6 секунд на один номер
        
        # Инициализация
        self._get_phone_number_id()
    
    def _get_phone_number_id(self):
        """Получение ID номера телефона"""
        waba_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
        if not waba_id:
            raise ValueError("WHATSAPP_BUSINESS_ACCOUNT_ID не найден в переменных окружения")
        
        url = f"{self.base_url}/{waba_id}/phone_numbers"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("data"):
                self.phone_number_id = data["data"][0]["id"]
                logger.info(f"Получен ID номера телефона: {self.phone_number_id}")
            else:
                raise ValueError("Не найдены номера телефонов")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении ID номера: {e}")
            raise
    
    def create_message_template(self, template_name: str, language: str = "ru", 
                               category: str = "MARKETING", components: List[Dict] = None):
        """Создание шаблона сообщения"""
        waba_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
        url = f"{self.base_url}/{waba_id}/message_templates"
        
        payload = {
            "name": template_name,
            "language": language,
            "category": category,
            "components": components or []
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Шаблон '{template_name}' создан с ID: {result.get('id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при создании шаблона: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Ответ сервера: {e.response.text}")
            raise
    
    def get_message_templates(self):
        """Получение списка шаблонов сообщений"""
        waba_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
        url = f"{self.base_url}/{waba_id}/message_templates"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Получено {len(data.get('data', []))} шаблонов")
            return data.get("data", [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении шаблонов: {e}")
            raise
    
    def send_template_message(self, to_number: str, template_name: str, 
                            language: str = "ru", components: List[Dict] = None):
        """Отправка шаблонного сообщения"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Сообщение отправлено на {to_number}, ID: {result.get('messages', [{}])[0].get('id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке сообщения на {to_number}: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Ответ сервера: {e.response.text}")
            raise
    
    def send_text_message(self, to_number: str, message_text: str):
        """Отправка простого текстового сообщения (только в активном окне беседы)"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Текстовое сообщение отправлено на {to_number}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке текста на {to_number}: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Ответ сервера: {e.response.text}")
            raise
    
    def bulk_send_template(self, recipients: List[str], template_name: str, 
                          language: str = "ru", components: List[Dict] = None,
                          delay_between_messages: float = 1.0):
        """Массовая отправка шаблонных сообщений"""
        results = []
        sent_count = 0
        failed_count = 0
        
        logger.info(f"Начало массовой рассылки для {len(recipients)} получателей")
        
        for i, recipient in enumerate(recipients):
            try:
                # Нормализация номера телефона
                normalized_number = self._normalize_phone_number(recipient)
                
                # Отправка сообщения
                result = self.send_template_message(
                    normalized_number, 
                    template_name, 
                    language, 
                    components
                )
                
                results.append({
                    "recipient": recipient,
                    "normalized_number": normalized_number,
                    "status": "success",
                    "message_id": result.get('messages', [{}])[0].get('id'),
                    "timestamp": datetime.now().isoformat()
                })
                
                sent_count += 1
                
                # Задержка между сообщениями
                if i < len(recipients) - 1:
                    time.sleep(delay_between_messages)
                
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение на {recipient}: {e}")
                results.append({
                    "recipient": recipient,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                failed_count += 1
                
                # Продолжаем даже при ошибке
                time.sleep(delay_between_messages)
        
        logger.info(f"Рассылка завершена. Отправлено: {sent_count}, Ошибок: {failed_count}")
        
        # Сохранение результатов
        self._save_results(results, template_name)
        
        return {
            "total": len(recipients),
            "sent": sent_count,
            "failed": failed_count,
            "results": results
        }
    
    def _normalize_phone_number(self, phone_number: str) -> str:
        """Нормализация номера телефона"""
        # Удаляем все нецифровые символы кроме +
        normalized = ''.join(char for char in phone_number if char.isdigit() or char == '+')
        
        # Если номер не начинается с +, добавляем его
        if not normalized.startswith('+'):
            normalized = '+' + normalized
        
        return normalized
    
    def _save_results(self, results: List[Dict], template_name: str):
        """Сохранение результатов рассылки в файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bulk_results_{template_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Результаты сохранены в файл: {filename}")
    
    def load_recipients_from_csv(self, csv_file: str, phone_column: str = "phone") -> List[str]:
        """Загрузка получателей из CSV файла"""
        recipients = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if phone_column in row and row[phone_column]:
                        recipients.append(row[phone_column])
            
            logger.info(f"Загружено {len(recipients)} номеров из {csv_file}")
            return recipients
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке CSV: {e}")
            raise
    
    def get_account_metrics(self):
        """Получение метрик аккаунта"""
        waba_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
        url = f"{self.base_url}/{waba_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Метрики аккаунта получены")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении метрик: {e}")
            raise


# Пример использования
if __name__ == "__main__":
    # Создание экземпляра класса
    sender = WhatsAppBulkSender()
    
    # Пример создания простого шаблона
    template_components = [
        {
            "type": "BODY",
            "text": "Привет! Это тестовое сообщение для рассылки."
        }
    ]
    
    try:
        # Создание шаблона (выполняется один раз)
        # sender.create_message_template(
        #     template_name="test_broadcast",
        #     language="ru",
        #     category="MARKETING",
        #     components=template_components
        # )
        
        # Получение существующих шаблонов
        templates = sender.get_message_templates()
        print("Доступные шаблоны:")
        for template in templates:
            print(f"- {template['name']} ({template['status']})")
        
        # Пример рассылки (раскомментируйте для использования)
        # recipients = ["+79000000000", "+79111111111"]  # Замените на реальные номера
        # result = sender.bulk_send_template(
        #     recipients=recipients,
        #     template_name="hello_world",  # Используйте существующий шаблон
        #     delay_between_messages=2.0
        # )
        # print(f"Результат рассылки: {result}")
        
    except Exception as e:
        logger.error(f"Ошибка в главной функции: {e}")
