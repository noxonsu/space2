from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any

def create_hr_dialogue_mimic_blueprint():
    """Создает Blueprint для API продукта HrDialogueMimic"""
    bp = Blueprint('hr_dialogue_mimic', __name__)
    
    @bp.route('/hr_dialogue_mimic/info', methods=['GET'])
    def get_product_info():
        """Получение информации о продукте"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('hr_dialogue_mimic')
            product_info = product.get_product_info()
            
            return jsonify({
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "product_info": product_info # Передаем полный product_info
            })
        except Exception as e:
            current_app.logger.error(f"Ошибка получения информации о продукте hr_dialogue_mimic: {e}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/hr_dialogue_mimic/demo', methods=['POST'])
    def execute_demo():
        """Выполнение демо-версии продукта"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('hr_dialogue_mimic')
            demo_params = request.get_json() or {}
            result = product.execute_demo(demo_params)
            
            return jsonify(result)
        except Exception as e:
            current_app.logger.error(f"Ошибка при выполнении демо hr_dialogue_mimic: {e}")
            return jsonify({"error": str(e), "status": "error"}), 500
    
    @bp.route('/hr_dialogue_mimic/create', methods=['POST'])
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
            
            product = product_factory.create_product('hr_dialogue_mimic')
            result = product.process_upload(files, form_data)
            
            return jsonify(result)
        except Exception as e:
            current_app.logger.error(f"Ошибка при обработке загрузки hr_dialogue_mimic: {e}")
            return jsonify({"error": str(e), "status": "error"}), 500
    
    return bp

# Экспорт для использования в main.py
hr_dialogue_mimic_bp = create_hr_dialogue_mimic_blueprint()
