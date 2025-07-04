"""
CLI команда для мониторинга Telegram канала и генерации продуктов
"""

import os
import sys
import argparse
import logging
import asyncio
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
    required_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_PHONE_NUMBER']
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
        api_id=os.getenv('TELEGRAM_API_ID'),
        api_hash=os.getenv('TELEGRAM_API_HASH'),
        phone_number=os.getenv('TELEGRAM_PHONE_NUMBER'),
        session_string=os.getenv('TELEGRAM_SESSION_STRING'),
        channel_username='@aideaxondemos'
    )
    
    return llm_service, product_generator, connector


def test_connection(connector):
    """Тестирование соединения с Telegram"""
    print("Тестируем соединение с Telegram API...")
    
    try:
        # Создаем и запускаем асинхронную функцию
        async def test_async():
            result = await connector.test_connection()
            # НЕ закрываем клиент здесь для дальнейшего использования
            return result
        
        result = asyncio.run(test_async())
        
        if result:
            print("✓ Соединение с Telegram API успешно")
            # Если сессия была создана, сохраняем её в .env
            if connector.session_string and not os.getenv('TELEGRAM_SESSION_STRING'):
                save_session_to_env(connector.session_string)
            return True
        else:
            print("✗ Ошибка соединения с Telegram API")
            return False
    except Exception as e:
        print(f"✗ Ошибка соединения с Telegram API: {e}")
        return False


def fetch_and_process_messages(connector, generator, limit=5):
    """Получение и обработка сообщений"""
    print(f"Получаем последние {limit} сообщений из канала...")
    
    try:
        # Создаем и запускаем асинхронную функцию
        async def fetch_async():
            return await connector.fetch_recent_messages(limit=limit)
        
        messages = asyncio.run(fetch_async())
        
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
    
    except Exception as e:
        print(f"Ошибка при получении сообщений: {e}")
        return


async def process_all_historical_messages_async(connector, generator):
    """Асинхронная обработка всех исторических сообщений из канала"""
    print("Начинаем обработку всех исторических сообщений из канала...")
    
    try:
        # Получаем все сообщения
        all_messages = await connector.fetch_all_messages()
        
        if not all_messages:
            return {
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "skipped_duplicates": 0,
                "products": [],
                "errors": [],
                "duplicates": []
            }
        
        print(f"Получено {len(all_messages)} сообщений для обработки")
        
        results = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "skipped_duplicates": 0,
            "products": [],
            "errors": [],
            "duplicates": []
        }
        
        for message in all_messages:
            # Фильтруем только содержательные сообщения
            if not generator._is_suitable_for_product_generation(message):
                continue
            
            results["processed"] += 1
            
            result = generator.generate_product_from_message(message)
            
            if result["success"]:
                results["successful"] += 1
                results["products"].append({
                    "product_id": result["product_id"],
                    "product_name": result["product_name"],
                    "message_id": result["message_id"]
                })
                print(f"Создан продукт: {result['product_id']}")
                
            elif "duplicate_product_id" in result:
                results["skipped_duplicates"] += 1
                results["duplicates"].append({
                    "message_id": result["message_id"],
                    "duplicate_of": result["duplicate_product_id"],
                    "error": result["error"]
                })
                print(f"Пропущен дубль: сообщение {result['message_id']}")
                
            else:
                results["failed"] += 1
                results["errors"].append({
                    "message_id": result["message_id"],
                    "error": result["error"]
                })
                print(f"Ошибка с сообщением {result['message_id']}: {result['error']}")
        
        print(f"\n=== РЕЗУЛЬТАТЫ ОБРАБОТКИ ===")
        print(f"Обработано сообщений: {results['processed']}")
        print(f"Успешно создано продуктов: {results['successful']}")
        print(f"Пропущено дубликатов: {results['skipped_duplicates']}")
        print(f"Ошибок: {results['failed']}")
        
        if results['products']:
            print(f"\n=== СОЗДАННЫЕ ПРОДУКТЫ ===")
            for product in results['products']:
                print(f"  • {product['product_id']}: {product['product_name']}")
        
        if results['duplicates']:
            print(f"\n=== ПРОПУЩЕННЫЕ ДУБЛИКАТЫ ===")
            for duplicate in results['duplicates']:
                print(f"  • Сообщение {duplicate['message_id']}: дубликат {duplicate['duplicate_of']}")
        
        if results['errors']:
            print(f"\n=== ОШИБКИ ===")
            for error in results['errors']:
                print(f"  • Сообщение {error.get('message_id', 'неизвестно')}: {error['error']}")
        
        print(f"\n=== ИТОГО ===")
        print(f"Новых продуктов создано: {results['successful']}")
        
        return results
        
    except Exception as e:
        print(f"Ошибка при обработке исторических сообщений: {e}")
        return {
            "processed": 0,
            "successful": 0,
            "failed": 1,
            "skipped_duplicates": 0,
            "products": [],
            "errors": [{"message_id": "неизвестно", "error": str(e)}],
            "duplicates": []
        }


def process_all_historical_messages(connector, generator):
    """Обработка всех исторических сообщений из канала"""
    print("Начинаем обработку всех исторических сообщений из канала...")
    
    async def process_async():
        try:
            # Получаем все сообщения
            all_messages = await connector.fetch_all_messages()
            
            if not all_messages:
                return {
                    "processed": 0,
                    "successful": 0,
                    "failed": 0,
                    "skipped_duplicates": 0,
                    "products": [],
                    "errors": [],
                    "duplicates": []
                }
            
            print(f"Получено {len(all_messages)} сообщений для обработки")
            
            results = {
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "skipped_duplicates": 0,
                "products": [],
                "errors": [],
                "duplicates": []
            }
            
            for message in all_messages:
                # Фильтруем только содержательные сообщения
                if not generator._is_suitable_for_product_generation(message):
                    continue
                
                results["processed"] += 1
                
                result = generator.generate_product_from_message(message)
                
                if result["success"]:
                    results["successful"] += 1
                    results["products"].append({
                        "product_id": result["product_id"],
                        "product_name": result["product_name"],
                        "message_id": result["message_id"]
                    })
                    print(f"Создан продукт: {result['product_id']}")
                    
                elif "duplicate_product_id" in result:
                    results["skipped_duplicates"] += 1
                    results["duplicates"].append({
                        "message_id": result["message_id"],
                        "duplicate_of": result["duplicate_product_id"],
                        "error": result["error"]
                    })
                    print(f"Пропущен дубль: сообщение {result['message_id']}")
                    
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "message_id": result["message_id"],
                        "error": result["error"]
                    })
                    print(f"Ошибка с сообщением {result['message_id']}: {result['error']}")
            
            # Закрываем клиент после обработки
            await connector.close()
            
            return results
            
        except Exception as e:
            print(f"Ошибка при обработке исторических сообщений: {e}")
            await connector.close()
            return {
                "processed": 0,
                "successful": 0,
                "failed": 1,
                "skipped_duplicates": 0,
                "products": [],
                "errors": [{"message_id": "неизвестно", "error": str(e)}],
                "duplicates": []
            }
    
    try:
        results = asyncio.run(process_async())
        
        print(f"\n=== РЕЗУЛЬТАТЫ ОБРАБОТКИ ===")
        print(f"Обработано сообщений: {results['processed']}")
        print(f"Успешно создано продуктов: {results['successful']}")
        print(f"Пропущено дубликатов: {results['skipped_duplicates']}")
        print(f"Ошибок: {results['failed']}")
        
        if results['products']:
            print(f"\n=== СОЗДАННЫЕ ПРОДУКТЫ ===")
            for product in results['products']:
                print(f"  • {product['product_id']}: {product['product_name']}")
        
        if results['duplicates']:
            print(f"\n=== ПРОПУЩЕННЫЕ ДУБЛИКАТЫ ===")
            for duplicate in results['duplicates']:
                print(f"  • Сообщение {duplicate['message_id']}: дубликат {duplicate['duplicate_of']}")
        
        if results['errors']:
            print(f"\n=== ОШИБКИ ===")
            for error in results['errors']:
                print(f"  • Сообщение {error.get('message_id', 'неизвестно')}: {error['error']}")
        
        print(f"\n=== ИТОГО ===")
        print(f"Новых продуктов создано: {results['successful']}")
        
        return results
        
    except Exception as e:
        print(f"Ошибка при обработке исторических сообщений: {e}")
        return None


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


def save_session_to_env(session_string):
    """Сохранение строки сессии в .env файл"""
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    
    try:
        # Читаем существующий .env файл
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Проверяем, есть ли уже строка с TELEGRAM_SESSION_STRING
        session_line_exists = False
        for i, line in enumerate(lines):
            if line.strip().startswith('TELEGRAM_SESSION_STRING='):
                lines[i] = f'TELEGRAM_SESSION_STRING={session_string}\n'
                session_line_exists = True
                break
        
        # Если строки нет, добавляем её
        if not session_line_exists:
            lines.append(f'TELEGRAM_SESSION_STRING={session_string}\n')
        
        # Записываем обратно в файл
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"✓ Строка сессии сохранена в .env файл")
        
    except Exception as e:
        print(f"⚠️  Не удалось сохранить сессию в .env файл: {e}")
        print(f"Пожалуйста, добавьте вручную в .env файл:")
        print(f"TELEGRAM_SESSION_STRING={session_string}")


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(description="Мониторинг Telegram канала для генерации продуктов")
    
    parser.add_argument(
        'action',
        choices=['test', 'fetch', 'monitor', 'process-all'],
        help='Действие: test (тест соединения), fetch (получить сообщения), monitor (непрерывный мониторинг), process-all (обработать все исторические сообщения)'
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
            
        elif args.action == 'process-all':
            # Создаем единый асинхронный контекст для process-all
            async def process_all_async():
                # Тестируем соединение
                if not await connector.test_connection():
                    return 1
                
                # Обрабатываем сообщения
                results = await process_all_historical_messages_async(connector, product_generator)
                
                # Закрываем клиент
                await connector.close()
                
                if results and results['successful'] > 0:
                    print(f"\n✅ Обработка завершена успешно! Создано {results['successful']} новых продуктов.")
                else:
                    print(f"\n⚠️  Обработка завершена без создания новых продуктов.")
                
                return 0
            
            try:
                exit_code = asyncio.run(process_all_async())
                sys.exit(exit_code)
            except Exception as e:
                print(f"Ошибка: {e}")
                sys.exit(1)
    
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        print("\nДобавьте в .env файл:")
        print("TELEGRAM_API_ID=ваш_api_id")
        print("TELEGRAM_API_HASH=ваш_api_hash")
        print("TELEGRAM_PHONE_NUMBER=ваш_номер_телефона")
        print("DEEPSEEK_API_KEY=ваш_ключ_deepseek")
        print("# TELEGRAM_SESSION_STRING будет добавлена автоматически после первого запуска")
        sys.exit(1)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
