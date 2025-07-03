#!/usr/bin/env python3
"""
WhatsApp Business API Admin Dashboard
Админ-панель для управления WhatsApp Business API
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'whatsapp-admin-secret-key-2025')

# Конфигурация
WHATSAPP_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'whatsapp_verify_token_2025')

class WhatsAppAPI:
    def __init__(self):
        self.access_token = WHATSAPP_ACCESS_TOKEN
        self.waba_id = WHATSAPP_BUSINESS_ACCOUNT_ID
        self.phone_number_id = WHATSAPP_PHONE_NUMBER_ID
        self.base_url = "https://graph.facebook.com/v23.0"
        
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_phone_numbers(self):
        """Получение номеров телефонов"""
        url = f"{self.base_url}/{self.waba_id}/phone_numbers"
        try:
            response = requests.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Error getting phone numbers: {e}")
        return []
    
    def get_message_templates(self):
        """Получение шаблонов сообщений"""
        url = f"{self.base_url}/{self.waba_id}/message_templates"
        try:
            response = requests.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Error getting templates: {e}")
        return []
    
    def send_template_message(self, to_number, template_name, from_phone_number_id, parameters=None):
        """Отправка шаблона сообщения"""
        url = f"{self.base_url}/{from_phone_number_id}/messages"
        
        template_data = {
            "name": template_name,
            "language": {"code": "en"}
        }
        
        if parameters:
            components = []
            # Добавляем параметры для body
            if parameters.get('body'):
                components.append({
                    "type": "body",
                    "parameters": [{"type": "text", "text": param} for param in parameters['body']]
                })
            
            # Добавляем параметры для кнопок
            if parameters.get('buttons'):
                for i, button_params in enumerate(parameters['buttons']):
                    components.append({
                        "type": "button",
                        "sub_type": "url",
                        "index": str(i),
                        "parameters": [{"type": "text", "text": param} for param in button_params]
                    })
            
            template_data["components"] = components
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "template",
            "template": template_data
        }
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=data)
            return response.status_code == 200, response.json()
        except Exception as e:
            logger.error(f"Error sending template: {e}")
            return False, {"error": str(e)}
    
    def get_subscribed_apps(self):
        """Получение подписанных приложений для WABA"""
        url = f"{self.base_url}/{self.waba_id}/subscribed_apps"
        try:
            response = requests.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return True, response.json().get('data', [])
            else:
                return False, response.json()
        except Exception as e:
            logger.error(f"Error getting subscribed apps: {e}")
            return False, {"error": str(e)}

# Инициализация API
whatsapp_api = WhatsAppAPI()

# База данных для хранения webhooks и сообщений
def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    # Таблица для webhooks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            webhook_data TEXT,
            message_id TEXT,
            status TEXT,
            from_number TEXT,
            to_number TEXT
        )
    ''')
    
    # Таблица для отправленных сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message_id TEXT,
            to_number TEXT,
            message_type TEXT,
            content TEXT,
            template_name TEXT,
            status TEXT DEFAULT 'sent'
        )
    ''')
    
    # Таблица для разговоров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE,
            last_message_time DATETIME,
            messages_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    conn.commit()
    conn.close()

# Инициализируем БД при запуске
init_db()

@app.route('/')
def dashboard():
    """Главная страница - дашборд"""
    phone_numbers = whatsapp_api.get_phone_numbers()
    templates = whatsapp_api.get_message_templates()
    
    # Статистика из БД
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    # Количество отправленных сообщений за последние 24 часа
    cursor.execute('''
        SELECT COUNT(*) FROM sent_messages 
        WHERE timestamp > datetime('now', '-1 day')
    ''')
    messages_24h = cursor.fetchone()[0]
    
    # Количество активных разговоров
    cursor.execute('''
        SELECT COUNT(*) FROM conversations 
        WHERE status = 'active'
    ''')
    active_conversations = cursor.fetchone()[0]
    
    # Последние webhooks
    cursor.execute('''
        SELECT * FROM webhooks 
        ORDER BY timestamp DESC 
        LIMIT 5
    ''')
    recent_webhooks = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'phone_numbers_count': len(phone_numbers),
        'templates_count': len(templates),
        'messages_24h': messages_24h,
        'active_conversations': active_conversations,
        'recent_webhooks': recent_webhooks
    }
    
    return render_template('dashboard.html', 
                         phone_numbers=phone_numbers, 
                         templates=templates,
                         stats=stats)

@app.route('/templates')
def templates_page():
    """Страница управления шаблонами"""
    templates = whatsapp_api.get_message_templates()
    return render_template('templates.html', templates=templates)

@app.route('/send_template', methods=['GET', 'POST'])
def send_template():
    """Отправка шаблона"""
    if request.method == 'POST':
        to_number = request.form.get('to_number')
        template_name = request.form.get('template_name')
        from_phone_number_id = request.form.get('from_phone_number_id')

        if not from_phone_number_id:
            flash('Не выбран номер отправителя!', 'error')
            return redirect(url_for('send_template'))
        
        # Параметры для шаблона
        parameters = {}
        if template_name == 'dashonoutrog_login':
            verification_code = request.form.get('verification_code') or str(random.randint(100000, 999999))
            parameters = {
                'body': [verification_code],
                'buttons': [[verification_code]]
            }
        
        success, result = whatsapp_api.send_template_message(to_number, template_name, from_phone_number_id, parameters)
        
        if success:
            # Сохраняем в БД
            conn = sqlite3.connect('whatsapp_admin.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sent_messages (message_id, to_number, message_type, content, template_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                result.get('messages', [{}])[0].get('id'),
                to_number,
                'template',
                json.dumps(parameters),
                template_name
            ))
            conn.commit()
            conn.close()
            
            flash(f'Шаблон {template_name} успешно отправлен на {to_number}', 'success')
        else:
            flash(f'Ошибка отправки: {result.get("error", {}).get("message", "Unknown error")}', 'error')
        
        return redirect(url_for('send_template'))
    
    templates = whatsapp_api.get_message_templates()
    phone_numbers = whatsapp_api.get_phone_numbers()
    return render_template('send_template.html', templates=templates, phone_numbers=phone_numbers)

@app.route('/webhooks')
def webhooks_page():
    """Страница просмотра webhooks"""
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM webhooks 
        ORDER BY timestamp DESC 
        LIMIT 50
    ''')
    webhooks = cursor.fetchall()
    conn.close()
    
    return render_template('webhooks.html', webhooks=webhooks)

@app.route('/conversations')
def conversations_page():
    """Страница просмотра разговоров"""
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM conversations 
        ORDER BY last_message_time DESC
    ''')
    conversations = cursor.fetchall()
    
    cursor.execute('''
        SELECT * FROM sent_messages 
        ORDER BY timestamp DESC 
        LIMIT 20
    ''')
    sent_messages = cursor.fetchall()
    
    conn.close()
    
    return render_template('conversations.html', 
                         conversations=conversations, 
                         sent_messages=sent_messages)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка входящих webhooks от WhatsApp"""
    data = request.get_json()
    
    # Сохраняем webhook в БД
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    # Извлекаем информацию из webhook
    webhook_data = json.dumps(data)
    message_id = None
    status = None
    from_number = None
    to_number = None
    
    if data and 'entry' in data:
        for entry in data['entry']:
            if 'changes' in entry:
                for change in entry['changes']:
                    if 'value' in change:
                        value = change['value']
                        
                        # Статусы сообщений
                        if 'statuses' in value:
                            for status_info in value['statuses']:
                                message_id = status_info.get('id')
                                status = status_info.get('status')
                                to_number = status_info.get('recipient_id')
                        
                        # Входящие сообщения
                        if 'messages' in value:
                            for message in value['messages']:
                                message_id = message.get('id')
                                from_number = message.get('from')
                                # Обновляем разговор
                                cursor.execute('''
                                    INSERT OR REPLACE INTO conversations 
                                    (phone_number, last_message_time, messages_count)
                                    VALUES (?, ?, COALESCE((SELECT messages_count FROM conversations WHERE phone_number = ?), 0) + 1)
                                ''', (from_number, datetime.now(), from_number))
    
    cursor.execute('''
        INSERT INTO webhooks (webhook_data, message_id, status, from_number, to_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (webhook_data, message_id, status, from_number, to_number))
    
    conn.commit()
    conn.close()
    
    logger.info(f"Webhook received: {data}")
    return jsonify({"status": "ok"})

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Верификация webhook"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge
    else:
        return 'Failed', 403

@app.route('/api/check_webhook_subscription')
def check_webhook_subscription():
    """API для проверки подписки на webhooks"""
    success, result = whatsapp_api.get_subscribed_apps()
    if success:
        return jsonify({"status": "ok", "subscribed_apps": result})
    else:
        return jsonify({"status": "error", "details": result}), 500

@app.route('/api/stats')
def api_stats():
    """API для получения статистики"""
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    
    # Статистика по дням за последнюю неделю
    cursor.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM sent_messages 
        WHERE timestamp > datetime('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    ''')
    daily_stats = cursor.fetchall()
    
    # Статистика по типам сообщений
    cursor.execute('''
        SELECT message_type, COUNT(*) as count
        FROM sent_messages 
        GROUP BY message_type
    ''')
    type_stats = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'daily_stats': daily_stats,
        'type_stats': type_stats
    })

@app.route('/api/simulate_webhook', methods=['POST'])
def simulate_webhook():
    """API для симуляции входящего webhook"""
    data = request.get_json()
    event_type = data.get('event_type')
    
    if not event_type:
        return jsonify({"status": "error", "message": "Event type is required"}), 400

    # Создаем тестовые данные
    timestamp = datetime.now()
    test_phone_number = "1234567890"
    message_id = f"wamid.test_{int(timestamp.timestamp())}"

    if event_type == 'status_delivered':
        webhook_body = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": WHATSAPP_BUSINESS_ACCOUNT_ID,
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {"display_phone_number": test_phone_number, "phone_number_id": WHATSAPP_PHONE_NUMBER_ID},
                        "statuses": [{
                            "id": message_id,
                            "status": "delivered",
                            "timestamp": str(int(timestamp.timestamp())),
                            "recipient_id": test_phone_number,
                            "conversation": {"id": "test_conv_id", "origin": {"type": "user_initiated"}}
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        status = "delivered"
        from_number = None
        to_number = test_phone_number

    elif event_type == 'incoming_message':
        webhook_body = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": WHATSAPP_BUSINESS_ACCOUNT_ID,
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {"display_phone_number": test_phone_number, "phone_number_id": WHATSAPP_PHONE_NUMBER_ID},
                        "messages": [{
                            "from": test_phone_number,
                            "id": message_id,
                            "timestamp": str(int(timestamp.timestamp())),
                            "text": {"body": "This is a test message"},
                            "type": "text"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        status = "received"
        from_number = test_phone_number
        to_number = None
    else:
        return jsonify({"status": "error", "message": "Unknown event type"}), 400

    # Сохраняем в БД
    conn = sqlite3.connect('whatsapp_admin.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO webhooks (webhook_data, message_id, status, from_number, to_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (json.dumps(webhook_body), message_id, status, from_number, to_number))
    conn.commit()
    conn.close()

    flash(f"Симуляция вебхука '{event_type}' прошла успешно!", 'success')
    return jsonify({"status": "ok"})


@app.route('/api/export_history')
def export_history():
    """API для экспорта истории сообщений и разговоров"""
    conn = sqlite3.connect('whatsapp_admin.db')
    conn.row_factory = sqlite3.Row  # Чтобы получать результаты в виде словарей
    cursor = conn.cursor()
    
    # Получаем все разговоры
    cursor.execute('''
        SELECT id, phone_number, last_message_time, messages_count, status
        FROM conversations 
        ORDER BY last_message_time DESC
    ''')
    conversations = [dict(row) for row in cursor.fetchall()]
    
    # Получаем все отправленные сообщения
    cursor.execute('''
        SELECT id, timestamp, message_id, to_number, message_type, content, template_name, status
        FROM sent_messages 
        ORDER BY timestamp DESC
    ''')
    sent_messages = [dict(row) for row in cursor.fetchall()]
    
    # Получаем webhooks (можно ограничить количество для оптимизации размера экспорта)
    cursor.execute('''
        SELECT id, timestamp, message_id, status, from_number, to_number
        FROM webhooks 
        ORDER BY timestamp DESC
        LIMIT 500
    ''')
    webhooks = [dict(row) for row in cursor.fetchall()]
    
    # Добавляем метаданные экспорта
    metadata = {
        'export_date': datetime.now().isoformat(),
        'version': '1.0',
        'phone_number_id': WHATSAPP_PHONE_NUMBER_ID,
        'business_account_id': WHATSAPP_BUSINESS_ACCOUNT_ID
    }
    
    conn.close()
    
    # Формируем финальный объект для экспорта
    export_data = {
        'metadata': metadata,
        'conversations': conversations,
        'sent_messages': sent_messages,
        'webhooks': webhooks
    }
    
    return jsonify(export_data)

if __name__ == '__main__':
    print("🚀 Запуск WhatsApp Business API Admin Dashboard")
    print(f"📞 Phone Number ID: {WHATSAPP_PHONE_NUMBER_ID}")
    print(f"🏢 WABA ID: {WHATSAPP_BUSINESS_ACCOUNT_ID}")
    print("🌐 Доступно по адресу: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
