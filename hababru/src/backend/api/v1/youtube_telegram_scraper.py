from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any

def create_youtube_telegram_scraper_blueprint():
    """Создает Blueprint для API продукта YoutubeTelegramScraper"""
    bp = Blueprint('youtube_telegram_scraper', __name__)
    
    @bp.route('/youtube_telegram_scraper/info', methods=['GET'])
    def get_product_info():
        """Получение информации о продукте"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('habab_youtube_telegram_scraper')
            product_info = product.get_product_info()
            
            return jsonify({
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "product_info": product_info # Передаем полный product_info
            })
        except Exception as e:
            current_app.logger.error(f"Ошибка получения информации о продукте youtube_telegram_scraper: {e}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/youtube_telegram_scraper/demo', methods=['POST'])
    def execute_demo():
        """Выполнение демо-версии продукта"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('habab_youtube_telegram_scraper')
            demo_params = request.get_json() or {}
            result = product.execute_demo(demo_params)
            
            return jsonify(result)
        except Exception as e:
            current_app.logger.error(f"Ошибка при выполнении демо youtube_telegram_scraper: {e}")
            return jsonify({"error": str(e), "status": "error"}), 500
    
    @bp.route('/youtube_telegram_scraper/create', methods=['POST'])
    def process_upload():
        """Обработка загруженных файлов и данных формы"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            # Получение файлов и данных формы
            files = {}
            for field_name in request.files:
                files[field_name] = request.files.getlist(field_name)
            
            form_data = request.form.to_dict()
            
            product = product_factory.create_product('habab_youtube_telegram_scraper')
            result = product.process_upload(files, form_data)
            
            return jsonify(result)
        except Exception as e:
            current_app.logger.error(f"Ошибка при обработке загрузки youtube_telegram_scraper: {e}")
            return jsonify({"error": str(e), "status": "error"}), 500
    
    return bp

# Экспорт для использования в main.py
youtube_telegram_scraper_bp = create_youtube_telegram_scraper_blueprint()
