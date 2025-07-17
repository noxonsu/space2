from flask import Blueprint, jsonify, request, current_app
import os
import logging
from datetime import datetime

browser_log_bp = Blueprint('browser_log', __name__)

@browser_log_bp.route('/log_browser_error', methods=['POST'])
def log_browser_error():
    app_logger = current_app.logger if current_app else logging.getLogger(__name__)
    app_logger.info("Received browser error log request.") # Добавлено для отладки
    data = request.get_json()
    message = data.get('message', 'No message provided')
    url = data.get('url', 'No URL provided')
    line = data.get('line', 'N/A')
    col = data.get('col', 'N/A')
    error_obj = data.get('error_obj', 'N/A')
    
    log_dir = os.path.join(current_app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, 'browser.log')
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (
        f"[{timestamp}] [BROWSER ERROR]\n"
        f"  Message: {message}\n"
        f"  URL: {url}\n"
        f"  Line: {line}, Col: {col}\n"
        f"  Error Object: {error_obj}\n"
        f"{'-'*50}\n"
    )
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        app_logger.error(f"Browser error logged to {log_file_path}: {message}")
        return jsonify({"status": "success", "message": "Log received"}), 200
    except Exception as e:
        app_logger.error(f"Failed to write browser log to file: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Failed to write log"}), 500
