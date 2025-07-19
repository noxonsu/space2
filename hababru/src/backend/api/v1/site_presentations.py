"""
API для создания презентационных сайтов
"""

import os
import io
import threading
import json
from flask import Blueprint, request, jsonify, current_app, Response
from werkzeug.utils import secure_filename

site_presentations_bp = Blueprint('site_presentations', __name__)

def get_product_factory():
    return current_app.config.get('PRODUCT_FACTORY')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'zip'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@site_presentations_bp.route('/create', methods=['POST'])
def create_presentation_site():
    """
    API endpoint для создания презентационного сайта
    """
    try:
        logger = current_app.logger
        logger.info("SitePresentations API: Получен запрос на создание сайта")
        
        # Получаем продукт из фабрики
        product_factory = get_product_factory()
        if not product_factory:
            return jsonify({
                'success': False,
                'error': 'Product factory не настроена'
            }), 500
        
        site_presentations_product = product_factory.create_product('site_presentations')
        if not site_presentations_product:
            return jsonify({
                'success': False,
                'error': 'Продукт презентационных сайтов не найден или не активен'
            }), 500
        
        # Обрабатываем загруженные файлы
        uploaded_files = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    uploaded_files.append(file_path)
                    logger.info(f"SitePresentations API: Сохранен файл {filename}")
        
        # Получаем дополнительные параметры
        telegram_contact = request.form.get('telegram_contact', '')
        company_name = request.form.get('company_name', '')
        
        if not uploaded_files:
            return jsonify({
                'success': False,
                'error': 'Необходимо загрузить хотя бы один файл презентации'
            }), 400
        
        # Формируем входные данные для продукта
        input_data = {
            'presentation_files': uploaded_files,
            'telegram_contact': telegram_contact,
            'company_name': company_name
        }
        
        logger.info(f"SitePresentations API: Запуск создания сайта с данными: {input_data}")
        
        # Выполняем создание сайта
        result = site_presentations_product.execute_demo(input_data)
        
        # Очищаем временные файлы
        for file_path in uploaded_files:
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"SitePresentations API: Не удалось удалить временный файл {file_path}: {e}")
        
        logger.info(f"SitePresentations API: Результат создания сайта: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"SitePresentations API: Ошибка создания сайта: {e}")
        return jsonify({
            'success': False,
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }), 500

@site_presentations_bp.route('/demo', methods=['POST'])
def demo_presentation_site():
    """
    Демо endpoint для создания сайта без загрузки файлов
    """
    try:
        logger = current_app.logger
        logger.info("SitePresentations API: Получен запрос на демо создание сайта")
        
        # Получаем продукт из фабрики
        product_factory = get_product_factory()
        if not product_factory:
            return jsonify({
                'success': False,
                'error': 'Product factory не настроена'
            }), 500
        
        site_presentations_product = product_factory.create_product('site_presentations')
        if not site_presentations_product:
            return jsonify({
                'success': False,
                'error': 'Продукт презентационных сайтов не найден или не активен'
            }), 500
        
        # Получаем параметры из JSON
        data = request.get_json() or {}
        telegram_contact = data.get('telegram_contact', '@demo_company')
        company_name = data.get('company_name', 'Demo Company')
        
        # Используем демо файлы
        input_data = {
            'presentation_files': ['demo_presentation.pdf', 'demo_brandbook.pdf'],
            'telegram_contact': telegram_contact,
            'company_name': company_name
        }
        
        logger.info(f"SitePresentations API: Запуск демо создания сайта")
        
        # Выполняем создание сайта
        result = site_presentations_product.execute_demo(input_data)
        
        logger.info(f"SitePresentations API: Результат демо создания сайта: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"SitePresentations API: Ошибка демо создания сайта: {e}")
        return jsonify({
            'success': False,
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }), 500

@site_presentations_bp.route('/info', methods=['GET'])
def get_product_info():
    """
    Получение информации о продукте презентационных сайтов
    """
    try:
        logger = current_app.logger
        logger.info("SitePresentations API: Запрос информации о продукте")
        
        # Получаем продукт из фабрики
        product_factory = get_product_factory()
        if not product_factory:
            return jsonify({
                'success': False,
                'error': 'Product factory не настроена'
            }), 500
        
        site_presentations_product = product_factory.create_product('site_presentations')
        if not site_presentations_product:
            return jsonify({
                'success': False,
                'error': 'Продукт презентационных сайтов не найден или не активен'
            }), 500
        
        # Получаем информацию о продукте
        product_info = site_presentations_product.get_product_info()
        demo_content = site_presentations_product.get_demo_content()
        input_interface = site_presentations_product.get_input_interface_description()
        output_interface = site_presentations_product.get_output_interface_description()
        
        result = {
            'success': True,
            'product_info': product_info,
            'demo_content': demo_content,
            'interfaces': {
                'input': input_interface,
                'output': output_interface
            }
        }
        
        logger.info("SitePresentations API: Информация о продукте получена")
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"SitePresentations API: Ошибка получения информации: {e}")
        return jsonify({
            'success': False,
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }), 500
