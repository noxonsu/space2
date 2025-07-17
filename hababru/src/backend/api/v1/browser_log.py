from flask import Blueprint, jsonify, request, current_app
import os
import logging
from datetime import datetime

browser_log_bp = Blueprint('browser_log', __name__)

@browser_log_bp.route('/log_browser_error', methods=['POST'])
def log_browser_error():
    app_logger = current_app.logger if current_app else logging.getLogger(__name__)
    
    try:
        data = request.get_json()
        if not data:
            app_logger.warning("Получен пустой запрос для логирования ошибки браузера")
            return jsonify({"status": "error", "message": "No data provided"}), 400
            
        message = data.get('message', 'No message provided')
        url = data.get('url', 'No URL provided')
        line = data.get('line', 'N/A')
        col = data.get('col', 'N/A')
        error_obj = data.get('error_obj', 'N/A')
        user_agent = request.headers.get('User-Agent', 'N/A')
        ip_address = request.remote_addr or 'N/A'
        
        app_logger.info(f"Received browser error log request from {ip_address}: {message}")
        
        log_dir = os.path.join(current_app.root_path, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, 'browser.log')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"[{timestamp}] [BROWSER ERROR]\n"
            f"  IP: {ip_address}\n"
            f"  User-Agent: {user_agent}\n"
            f"  Message: {message}\n"
            f"  URL: {url}\n"
            f"  Line: {line}, Col: {col}\n"
            f"  Error Object: {error_obj}\n"
            f"{'-'*80}\n"
        )
        
        try:
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            app_logger.info(f"Browser error logged to {log_file_path}: {message[:100]}...")
            return jsonify({"status": "success", "message": "Log received"}), 200
        except Exception as file_error:
            app_logger.error(f"Failed to write browser log to file: {file_error}", exc_info=True)
            return jsonify({"status": "error", "message": "Failed to write log"}), 500
            
    except Exception as e:
        app_logger.error(f"Error processing browser log request: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Internal server error"}), 500
