"""
CLI команда для мониторинга Telegram канала и генерации продуктов
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.backend.services.telegram_connector import TelegramConnector, TelegramMonitor
from src.backend.services.telegram_product_generator import TelegramProductGenerator
from src.backend.services.llm_service import LLMService
from dotenv import load_dotenv


def setup_logging(level=logging.INFO):
    """Настройка логирования"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('telegram_monitor.log')
        ]
    )


def load_environment():
    """Загрузка переменных окружения"""
    # Ищем .env файл в корне проекта
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    load_dotenv(env_path)
    
    # Проверяем необходимые переменные
    required_vars = ['TELEGRAM_BOT_TOKEN', 'DEEPSEEK_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")


def create_services():
    """Создание экземпляров сервисов"""
    # LLM сервис
    llm_service = LLMService(
        deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Генератор продуктов
    product_generator = TelegramProductGenerator(llm_service=llm_service)
    
    # Telegram коннектор
    connector = TelegramConnector(
        bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
        channel_username='@aideaxondemos'
    )
    
    return llm_service, product_generator, connector


def test_connection(connector):
    """Тестирование соединения с Telegram"""
    print("Тестируем соединение с Telegram API...")
    
    if connector.test_connection():
        print("✓ Соединение с Telegram API успешно")
        return True
    else:
        print("✗ Ошибка соединения с Telegram API")
        return False


def fetch_and_process_messages(connector, generator, limit=5):
    """Получение и обработка сообщений"""
    print(f"Получаем последние {limit} сообщений из канала...")
    
    messages = connector.fetch_recent_messages(limit=limit)
    
    if not messages:
        print("Сообщения не найдены")
        return
    
    print(f"Найдено {len(messages)} сообщений")
    
    for i, message in enumerate(messages, 1):
        print(f"\nСообщение {i}:")
        print(f"  ID: {message.message_id}")
        print(f"  Дата: {message.date}")
        print(f"  Текст: {message.text[:100]}{'...' if len(message.text) > 100 else ''}")
        print(f"  Медиа: {len(message.media_files)} файлов")
    
    # Спрашиваем у пользователя какие сообщения обработать
    process_choice = input(f"\nОбработать все сообщения? (y/n/числа через запятую): ").strip().lower()
    
    if process_choice == 'n':
        return
    elif process_choice == 'y':
        messages_to_process = messages
    else:
        try:
            indices = [int(x.strip()) - 1 for x in process_choice.split(',')]
            messages_to_process = [messages[i] for i in indices if 0 <= i < len(messages)]
        except:
            print("Неверный формат. Обрабатываем все сообщения.")
            messages_to_process = messages
    
    if not messages_to_process:
        print("Нет сообщений для обработки")
        return
    
    print(f"\nОбрабатываем {len(messages_to_process)} сообщений...")
    
    results = generator.process_batch_messages(messages_to_process)
    
    print(f"\nРезультаты обработки:")
    print(f"  Обработано: {results['processed']}")
    print(f"  Успешно: {results['successful']}")
    print(f"  Ошибок: {results['failed']}")
    
    if results['products']:
        print(f"\nСозданные продукты:")
        for product in results['products']:
            print(f"  - {product['product_id']}: {product['product_name']}")
    
    if results['errors']:
        print(f"\nОшибки:")
        for error in results['errors']:
            print(f"  - Сообщение {error['message_id']}: {error['error']}")


def start_monitoring(connector, generator, interval=300):
    """Запуск непрерывного мониторинга"""
    print(f"Запускаем мониторинг канала (интервал: {interval} секунд)")
    print("Для остановки нажмите Ctrl+C")
    
    monitor = TelegramMonitor(
        connector=connector,
        product_generator=generator,
        check_interval=interval
    )
    
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nОстанавливаем мониторинг...")
        monitor.stop_monitoring()


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(description="Мониторинг Telegram канала для генерации продуктов")
    
    parser.add_argument(
        'action',
        choices=['test', 'fetch', 'monitor'],
        help='Действие: test (тест соединения), fetch (получить сообщения), monitor (непрерывный мониторинг)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='Количество сообщений для получения (по умолчанию: 5)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Интервал мониторинга в секундах (по умолчанию: 300)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Подробный вывод'
    )
    
    args = parser.parse_args()
    
    # Настройка логирования
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    try:
        # Загрузка переменных окружения
        load_environment()
        
        # Создание сервисов
        llm_service, product_generator, connector = create_services()
        
        # Выполнение действия
        if args.action == 'test':
            if test_connection(connector):
                print("Система готова к работе")
            else:
                sys.exit(1)
                
        elif args.action == 'fetch':
            if not test_connection(connector):
                sys.exit(1)
            fetch_and_process_messages(connector, product_generator, args.limit)
            
        elif args.action == 'monitor':
            if not test_connection(connector):
                sys.exit(1)
            start_monitoring(connector, product_generator, args.interval)
    
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        print("\nДобавьте в .env файл:")
        print("TELEGRAM_BOT_TOKEN=ваш_токен_бота")
        print("DEEPSEEK_API_KEY=ваш_ключ_deepseek")
        sys.exit(1)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
