from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import os
import json
import csv
from datetime import datetime
from whatsapp_bulk_sender import WhatsAppBulkSender
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Инициализация отправителя
sender = WhatsAppBulkSender()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/templates')
def templates():
    """Страница управления шаблонами"""
    try:
        templates = sender.get_message_templates()
        return render_template('templates.html', templates=templates)
    except Exception as e:
        flash(f'Ошибка при получении шаблонов: {str(e)}', 'error')
        return render_template('templates.html', templates=[])

@app.route('/create_template', methods=['GET', 'POST'])
def create_template():
    """Создание нового шаблона"""
    if request.method == 'POST':
        try:
            template_name = request.form['template_name']
            language = request.form.get('language', 'ru')
            category = request.form.get('category', 'MARKETING')
            body_text = request.form['body_text']
            
            # Создание компонентов шаблона
            components = [
                {
                    "type": "BODY",
                    "text": body_text
                }
            ]
            
            # Добавляем заголовок, если указан
            if request.form.get('header_text'):
                components.insert(0, {
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": request.form['header_text']
                })
            
            # Добавляем футер, если указан
            if request.form.get('footer_text'):
                components.append({
                    "type": "FOOTER",
                    "text": request.form['footer_text']
                })
            
            result = sender.create_message_template(
                template_name=template_name,
                language=language,
                category=category,
                components=components
            )
            
            flash(f'Шаблон "{template_name}" создан успешно!', 'success')
            return redirect(url_for('templates'))
            
        except Exception as e:
            flash(f'Ошибка при создании шаблона: {str(e)}', 'error')
    
    return render_template('create_template.html')

@app.route('/bulk_send', methods=['GET', 'POST'])
def bulk_send():
    """Страница массовой рассылки"""
    if request.method == 'POST':
        try:
            template_name = request.form['template_name']
            recipients_text = request.form.get('recipients_text', '')
            delay = float(request.form.get('delay', 1.0))
            
            # Обработка списка получателей
            recipients = []
            if recipients_text:
                recipients = [line.strip() for line in recipients_text.split('\n') if line.strip()]
            
            # Загрузка из CSV файла, если он был загружен
            if 'csv_file' in request.files:
                csv_file = request.files['csv_file']
                if csv_file and csv_file.filename:
                    # Сохраняем временный файл
                    csv_path = f"temp_{csv_file.filename}"
                    csv_file.save(csv_path)
                    
                    # Загружаем получателей из CSV
                    csv_recipients = sender.load_recipients_from_csv(
                        csv_path, 
                        request.form.get('phone_column', 'phone')
                    )
                    recipients.extend(csv_recipients)
                    
                    # Удаляем временный файл
                    os.remove(csv_path)
            
            if not recipients:
                flash('Не указаны получатели для рассылки', 'error')
                return redirect(url_for('bulk_send'))
            
            # Выполнение рассылки
            result = sender.bulk_send_template(
                recipients=recipients,
                template_name=template_name,
                delay_between_messages=delay
            )
            
            flash(f'Рассылка завершена! Отправлено: {result["sent"]}, Ошибок: {result["failed"]}', 'success')
            return render_template('bulk_send_result.html', result=result)
            
        except Exception as e:
            flash(f'Ошибка при рассылке: {str(e)}', 'error')
    
    # Получаем список доступных шаблонов
    try:
        templates = sender.get_message_templates()
        approved_templates = [t for t in templates if t.get('status') == 'APPROVED']
    except Exception as e:
        approved_templates = []
        flash(f'Ошибка при получении шаблонов: {str(e)}', 'warning')
    
    return render_template('bulk_send.html', templates=approved_templates)

@app.route('/metrics')
def metrics():
    """Страница метрик"""
    try:
        metrics = sender.get_account_metrics()
        return render_template('metrics.html', metrics=metrics)
    except Exception as e:
        flash(f'Ошибка при получении метрик: {str(e)}', 'error')
        return render_template('metrics.html', metrics={})

@app.route('/api/send_test_message', methods=['POST'])
def send_test_message():
    """API для отправки тестового сообщения"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        template_name = data.get('template_name')
        
        if not phone_number or not template_name:
            return jsonify({'error': 'Не указан номер телефона или имя шаблона'}), 400
        
        result = sender.send_template_message(phone_number, template_name)
        
        return jsonify({
            'success': True,
            'message_id': result.get('messages', [{}])[0].get('id'),
            'message': 'Сообщение отправлено успешно'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates')
def api_templates():
    """API для получения списка шаблонов"""
    try:
        templates = sender.get_message_templates()
        return jsonify(templates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_example_csv')
def download_example_csv():
    """Скачивание примера CSV файла"""
    example_data = [
        ['name', 'phone', 'email'],
        ['Иван Иванов', '+79001234567', 'ivan@example.com'],
        ['Петр Петров', '+79007654321', 'petr@example.com'],
        ['Мария Сидорова', '+79009876543', 'maria@example.com']
    ]
    
    # Создаем временный CSV файл
    csv_filename = 'example_recipients.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(example_data)
    
    return send_file(csv_filename, as_attachment=True, download_name='example_recipients.csv')

if __name__ == '__main__':
    # Создаем директорию для шаблонов если её нет
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
