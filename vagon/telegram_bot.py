import os
import logging
import pandas as pd
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from dotenv import load_dotenv
import requests
import io
import base64

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# URL вашего локального Flask API
# В Codespaces используем локальный адрес, так как бот работает в том же контейнере
API_URL = "http://127.0.0.1:8080"

# --- Вспомогательные функции для взаимодействия с API ---

async def call_api(endpoint, method='GET', json_data=None):
    try:
        if method == 'GET':
            response = requests.get(f"{API_URL}/{endpoint}")
        elif method == 'POST':
            response = requests.post(f"{API_URL}/{endpoint}", json=json_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Ошибка при подключении к API {endpoint}: {e}"
        if e.response is not None:
            try:
                error_details = e.response.json().get('error', e.response.text)
                error_message = f"Ошибка при подключении к API {endpoint}: {error_details}"
            except ValueError:
                error_message = f"Ошибка при подключении к API {endpoint}: Не удалось декодировать JSON. Ответ: {e.response.text}"
        logger.error(error_message)
        raise Exception(error_message)

# --- Команды бота ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я бот для анализа данных портового терминала. "
        "Отправьте мне запрос на естественном языке, и я сгенерирую и выполню SQL-запрос, а также построю график, если это возможно."
        "\n\nИспользуйте /help для получения списка команд."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с помощью при команде /help."""
    help_text = (
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Показать это сообщение\n"
        "/models - Показать доступные LLM модели\n"
        "/set_model <model_name> - Установить LLM модель (например, /set_model Qwen/Qwen2.5-Coder-7B)\n"
        "/stats - Получить статистику по таблицам базы данных\n"
        "\nПросто отправьте мне ваш запрос на естественном языке, например:\n"
        "'Покажи 5 самых тяжелых грузов, принятых в этом месяце.'\n"
        "'Сделай график выгрузки вагонов по месяцам за последний год.'"
    )
    await update.message.reply_text(help_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает и отправляет статистику по таблицам."""
    try:
        stats = await call_api("api/stats")
        if stats:
            df_stats = pd.DataFrame(stats)
            # Форматируем для читаемости в Telegram
            response_text = "📊 **Статистика по таблицам:**\n\n"
            for _, row in df_stats.iterrows():
                response_text += (
                    f"**База данных:** `{row['DATABASE_NAME']}`\n"
                    f"**Таблица:** `{row['TABLE_NAME']}`\n"
                    f"**Записей:** `{row['TABLE_ROWS']:,}`\n"
                    f"**Размер (MB):** `{row['SIZE_MB']:.2f}`\n\n"
                )
            await update.message.reply_text(response_text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Не удалось загрузить статистику по таблицам.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении статистики: {e}")

async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает доступные LLM модели и текущую."""
    try:
        models_info = await call_api("api/models")
        if models_info:
            available_models = models_info.get('models', [])
            current_model = models_info.get('current_model')
            
            response_text = "🤖 **Доступные LLM модели:**\n"
            for model in available_models:
                response_text += f"- `{model}`\n"
            response_text += f"\n**Текущая модель:** `{current_model}`"
            
            await update.message.reply_text(response_text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Не удалось загрузить информацию о моделях.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении моделей: {e}")

async def set_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Устанавливает LLM модель."""
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите имя модели. Например: `/set_model Qwen/Qwen2.5-Coder-7B`")
        return
    
    model_name = " ".join(context.args)
    try:
        result = await call_api("api/models/set", method='POST', json_data={'model_name': model_name})
        if result.get('success'):
            await update.message.reply_text(f"✅ Модель успешно изменена на `{result['current_model']}`.", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Не удалось установить модель: {result.get('error', 'Неизвестная ошибка')}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при установке модели: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текстовые сообщения пользователя, генерирует SQL и выполняет его."""
    user_query = update.message.text
    await update.message.reply_text("⏳ Ваш запрос обрабатывается. Это может занять некоторое время...")

    try:
        # Шаг 1: Генерация SQL
        await update.message.reply_text("🤖 Генерирую SQL-запрос...")
        sql_response = await call_api("api/generate-sql-with-prompt", method='POST', json_data={"query": user_query})
        sql_query = sql_response.get("sql_query")
        full_prompt = sql_response.get("full_prompt")

        if not sql_query:
            await update.message.reply_text("❌ Не удалось сгенерировать SQL-запрос. Попробуйте перефразировать.")
            return

        await update.message.reply_text(f"✅ **Сгенерированный SQL-запрос:**\n```sql\n{sql_query}\n```", parse_mode='Markdown')
        
        # Сохраняем SQL и полный промпт для возможного дебага
        context.user_data['last_sql_query'] = sql_query
        context.user_data['last_full_prompt'] = full_prompt
        context.user_data['last_user_query'] = user_query

        # Шаг 2: Выполнение SQL и получение данных/графика
        await update.message.reply_text("📊 Выполняю запрос и строю график...")
        execute_response = await call_api("api/execute-sql-with-chart", method='POST', json_data={
            "query": sql_query,
            "user_query": user_query,
            "create_chart": True # Всегда пытаемся создать график
        })
        
        data = execute_response.get("data")
        chart_base64 = execute_response.get("chart")
        chart_type = execute_response.get("chart_type")

        if data:
            df_results = pd.DataFrame(data)
            # Отправляем первые 10 строк данных, если их много
            if len(df_results) > 10:
                await update.message.reply_text(f"📈 **Первые 10 строк результата:**\n```\n{df_results.head(10).to_string(index=False)}\n```", parse_mode='Markdown')
                # Предлагаем скачать полный CSV
                csv_buffer = io.StringIO()
                df_results.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv_buffer.seek(0)
                await update.message.reply_document(
                    document=csv_buffer.getvalue().encode('utf-8'),
                    filename="query_results.csv",
                    caption="Полный результат запроса в CSV."
                )
            else:
                await update.message.reply_text(f"📈 **Результат запроса:**\n```\n{df_results.to_string(index=False)}\n```", parse_mode='Markdown')
            
            if chart_base64:
                try:
                    chart_bytes = base64.b64decode(chart_base64)
                    await update.message.reply_photo(
                        photo=chart_bytes,
                        caption=f"График типа: {chart_type}"
                    )
                except Exception as chart_e:
                    logger.error(f"Ошибка при декодировании/отправке графика: {chart_e}")
                    await update.message.reply_text("❌ Не удалось отобразить график.")
            else:
                await update.message.reply_text("ℹ️ График не был сгенерирован (возможно, недостаточно данных или тип запроса не подходит для визуализации).")
        else:
            await update.message.reply_text("ℹ️ Запрос не вернул данных.")

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await update.message.reply_text(f"❌ Произошла ошибка при обработке вашего запроса: {e}")
        # Предлагаем дебаг, если есть сохраненный промпт
        if 'last_full_prompt' in context.user_data:
            keyboard = [[InlineKeyboardButton("Показать полный промпт", callback_data="show_full_prompt")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Возможно, это поможет в отладке:", reply_markup=reply_markup)

async def show_full_prompt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает колбэк для показа полного промпта."""
    query = update.callback_query
    await query.answer() # Отвечаем на колбэк, чтобы убрать "часики"
    
    full_prompt = context.user_data.get('last_full_prompt', 'Промпт не найден.')
    user_query = context.user_data.get('last_user_query', 'Запрос пользователя не найден.')
    sql_query = context.user_data.get('last_sql_query', 'SQL-запрос не найден.')

    response_text = (
        "--- **Детали последнего запроса** ---\n\n"
        f"**Запрос пользователя:**\n```\n{user_query}\n```\n\n"
        f"**Сгенерированный SQL:**\n```sql\n{sql_query}\n```\n\n"
        f"**Полный промпт, отправленный LLM:**\n```\n{full_prompt}\n```"
    )
    
    # Разбиваем длинный текст на части, если он превышает лимит Telegram
    if len(response_text) > 4096:
        parts = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
        for part in parts:
            await query.message.reply_text(part, parse_mode='Markdown')
    else:
        await query.message.reply_text(response_text, parse_mode='Markdown')


def main() -> None:
    """Запускает бота."""
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        logger.error("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")
        print("ОШИБКА: Переменная окружения TELEGRAM_BOT_TOKEN не установлена. Бот не может быть запущен.")
        print("Пожалуйста, добавьте TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_БОТА в файл .env")
        return

    application = Application.builder().token(telegram_token).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("models", models_command))
    application.add_handler(CommandHandler("set_model", set_model_command))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик колбэков
    application.add_handler(CallbackQueryHandler(show_full_prompt_callback, pattern="show_full_prompt"))

    logger.info("Бот запущен. Ожидание сообщений...")
    print("Telegram бот запущен. Ожидание сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
