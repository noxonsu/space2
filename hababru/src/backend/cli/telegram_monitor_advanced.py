"""
Улучшенный CLI для мониторинга Telegram канала и генерации продуктов
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
            logging.FileHandler('telegram_monitor_advanced.log')
        ]
    )


def load_environment():
    """Загрузка переменных окружения"""
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    load_dotenv(env_path)
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'DEEPSEEK_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")


def create_services():
    """Создание всех необходимых сервисов"""
    # LLM Service
    llm_service = LLMService(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        model=os.getenv('DEEPSEEK_MODEL', 'deepseek-chat'),
        base_url=os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    )
    
    # Telegram Connector
    connector = TelegramConnector(
        bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
        channel_username=os.getenv('TELEGRAM_CHANNEL', 'aideaxondemos')
    )
    
    # Product Generator
    generator = TelegramProductGenerator(llm_service=llm_service)
    
    return llm_service, connector, generator


def run_historical_processing(connector: TelegramConnector, generator: TelegramProductGenerator):
    """Обработка всех исторических сообщений"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Начинаем обработку всех исторических сообщений")
        
        # Проверяем соединение
        if not connector.test_connection():
            logger.error("Не удалось подключиться к Telegram API")
            return
        
        # Обрабатываем все сообщения
        results = generator.process_all_historical_messages(connector)
        
        # Выводим детальную статистику
        logger.info("=== РЕЗУЛЬТАТЫ ОБРАБОТКИ ИСТОРИЧЕСКИХ СООБЩЕНИЙ ===")
        logger.info(f"Обработано сообщений: {results['processed']}")
        logger.info(f"Успешно создано продуктов: {results['successful']}")
        logger.info(f"Пропущено дублей: {results['skipped_duplicates']}")
        logger.info(f"Ошибок: {results['failed']}")
        
        if results['products']:
            logger.info("\n📦 СОЗДАННЫЕ ПРОДУКТЫ:")
            for product in results['products']:
                logger.info(f"  ✅ {product['product_id']}: {product['product_name']} (из сообщения {product['message_id']})")
        
        if results['duplicates']:
            logger.info("\n🔄 ПРОПУЩЕННЫЕ ДУБЛИ:")
            for duplicate in results['duplicates']:
                logger.info(f"  ⚠️  Сообщение {duplicate['message_id']}: дубль продукта {duplicate['duplicate_of']}")
        
        if results['errors']:
            logger.warning("\n❌ ОШИБКИ:")
            for error in results['errors']:
                if 'message_id' in error:
                    logger.warning(f"  ❌ Сообщение {error['message_id']}: {error['error']}")
                else:
                    logger.warning(f"  ❌ {error['error']}")
        
        logger.info(f"\n🎯 ИТОГ: Создано {results['successful']} новых продуктов, пропущено {results['skipped_duplicates']} дублей")
        
        # Показываем список всех продуктов в системе
        logger.info("\n📋 ВСЕ ПРОДУКТЫ В СИСТЕМЕ:")
        all_products = generator._get_existing_products_with_data()
        for product_id, product_data in all_products.items():
            logger.info(f"  📄 {product_id}: {product_data.get('name', 'Без названия')}")
        
    except Exception as e:
        logger.error(f"Ошибка обработки исторических сообщений: {e}")


def run_batch_generation(connector: TelegramConnector, generator: TelegramProductGenerator, limit: int):
    """Генерация продуктов из последних сообщений"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Получение {limit} последних сообщений")
        
        if not connector.test_connection():
            logger.error("Не удалось подключиться к Telegram API")
            return
        
        messages = connector.fetch_recent_messages(limit=limit)
        if not messages:
            logger.warning("Сообщения не найдены")
            return
        
        logger.info(f"Получено {len(messages)} сообщений")
        
        # Фильтруем подходящие сообщения
        suitable_messages = []
        for msg in messages:
            if generator._is_suitable_for_product_generation(msg):
                suitable_messages.append(msg)
                logger.info(f"  ✅ Сообщение {msg.message_id}: подходит для генерации")
            else:
                logger.info(f"  ❌ Сообщение {msg.message_id}: не подходит для генерации")
        
        logger.info(f"Из них подходят для генерации: {len(suitable_messages)}")
        
        if suitable_messages:
            results = generator.process_batch_messages(suitable_messages)
            
            logger.info("=== РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ ===")
            logger.info(f"Обработано: {results['processed']}")
            logger.info(f"Успешно: {results['successful']}")
            logger.info(f"Ошибок: {results['failed']}")
            
            if results['products']:
                logger.info("Созданные продукты:")
                for product in results['products']:
                    logger.info(f"  ✅ {product['product_id']}: {product['product_name']}")
        else:
            logger.info("Подходящих сообщений для генерации не найдено")
        
    except Exception as e:
        logger.error(f"Ошибка пакетной генерации: {e}")


def run_monitoring(connector: TelegramConnector, generator: TelegramProductGenerator, interval: int):
    """Запуск мониторинга"""
    logger = logging.getLogger(__name__)
    
    try:
        monitor = TelegramMonitor(connector, generator, check_interval=interval)
        
        logger.info(f"🚀 Запуск мониторинга с интервалом {interval} секунд")
        logger.info("Нажмите Ctrl+C для остановки")
        
        monitor.start_monitoring()
        
    except Exception as e:
        logger.error(f"Ошибка мониторинга: {e}")


def check_duplicates(generator: TelegramProductGenerator):
    """Проверка и отображение информации о существующих продуктах"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔍 АНАЛИЗ СУЩЕСТВУЮЩИХ ПРОДУКТОВ")
        
        all_products = generator._get_existing_products_with_data()
        
        if not all_products:
            logger.info("В системе нет продуктов")
            return
        
        logger.info(f"Найдено {len(all_products)} продуктов:")
        
        for product_id, product_data in all_products.items():
            name = product_data.get('name', 'Без названия')
            description = product_data.get('description', 'Без описания')
            category = product_data.get('category', 'Без категории')
            
            logger.info(f"\n📄 {product_id}")
            logger.info(f"   Название: {name}")
            logger.info(f"   Описание: {description}")
            logger.info(f"   Категория: {category}")
            
            # Показываем ключевые слова для поиска дублей
            keywords = product_data.get('seo', {}).get('keywords', [])
            if keywords:
                logger.info(f"   Ключевые слова: {', '.join(keywords[:3])}...")
        
    except Exception as e:
        logger.error(f"Ошибка анализа продуктов: {e}")


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(description='Продвинутый Telegram мониторинг и генерация продуктов')
    parser.add_argument('--mode', choices=['monitor', 'generate', 'historical', 'check'], 
                       default='monitor', help='Режим работы')
    parser.add_argument('--limit', type=int, default=10, 
                       help='Лимит сообщений для обработки')
    parser.add_argument('--channel', default='aideaxondemos', 
                       help='Username Telegram канала')
    parser.add_argument('--interval', type=int, default=300,
                       help='Интервал мониторинга в секундах')
    parser.add_argument('--debug', action='store_true',
                       help='Включить отладочное логирование')
    
    args = parser.parse_args()
    
    # Настройка логирования
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    
    try:
        # Загрузка конфигурации
        load_environment()
        logger.info("✅ Переменные окружения загружены")
        
        # Создание сервисов
        llm_service, connector, generator = create_services()
        connector.channel_username = args.channel
        
        if args.mode == 'monitor':
            logger.info(f"🔄 Запуск мониторинга канала @{args.channel}")
            run_monitoring(connector, generator, args.interval)
            
        elif args.mode == 'generate':
            logger.info(f"⚡ Генерация продуктов из {args.limit} последних сообщений")
            run_batch_generation(connector, generator, args.limit)
            
        elif args.mode == 'historical':
            logger.info(f"📚 Обработка всех исторических сообщений из канала @{args.channel}")
            run_historical_processing(connector, generator)
            
        elif args.mode == 'check':
            logger.info("🔍 Проверка существующих продуктов")
            check_duplicates(generator)
            
    except KeyboardInterrupt:
        logger.info("⏹️  Остановка по запросу пользователя")
    except Exception as e:
        logger.error(f"❌ Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
