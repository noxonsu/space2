# B2B Платформа для Кастомных Решений с SEO-Фокусом

## Описание Проекта

Данная платформа представляет собой B2B-сервис, специализирующийся на разработке кастомных решений для бизнеса. Основная цель — привлечение клиентов через SEO-оптимизированные демонстрационные сервисы, которые показывают экспертизу команды в различных отраслях.

### Ключевые Направления:
- **Анализ юридических документов** - Демонстрационный сервис для проверки договоров с AI-анализом
- **Мониторинг отраслевых новостей** - Система отслеживания упоминаний и анализа новостей (например, ВЭД)
- **Кастомные B2B-решения** - Разработка под конкретные задачи клиентов

### Архитектура Платформы:
Платформа построена на принципе **SEO-first подхода**, где каждый демонстрационный сервис окружен семантическим ядром целевых страниц для привлечения органического трафика и демонстрации экспертности.

### Текущий Модуль: Анализ Договоров
Пользователь загружает текст договора (PDF/DOC), система асинхронно анализирует каждый пункт/абзац с помощью LLM, отображая потенциальные риски, рекомендации и связи между разделами документа.

Сервис использует универсальный LLM-коннектор (DeepSeek/OpenAI), кэширует результаты для производительности и генерирует SEO-оптимизированные страницы для каждого типа договоров.

## Запуск Приложения

Для запуска Flask-application выполните следующие шаги:

1.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Настройте переменные окружения:**
    Скопируйте `.env.example` в `.env` и заполните необходимые API-ключи и другие параметры.
    ```bash
    cp .env.example .env
    ```
3.  **Запустите приложение:**
    ```bash
    python -m src.backend.main
    ```
    Приложение будет доступно по адресу `http://127.0.0.1:5001`.
    
    **Важно:** Если вы работаете в Codespaces, приложение будет доступно по динамическому URL, который Codespaces предоставляет для порта 5001.

## Работа в Codespaces и Тестирование

### Основная среда разработки
Мы работаем преимущественно в **GitHub Codespaces**. Это означает, что приложения должны быть настроены для работы в облачной среде, а не на локальной машине.

**Ключевые моменты:**
- **Сетевые настройки:** Приложения должны запускаться на `0.0.0.0`, чтобы быть доступными извне контейнера.
- **URL и порты:** Вместо `localhost` используйте динамически генерируемые URL, которые предоставляет Codespaces. Для этого используйте переменные окружения, такие как `CODESPACE_NAME` и `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`.
- **Автоматизация:** Настройте скрипты так, чтобы они автоматически определяли, что запущены в Codespaces, и применяли соответствующие конфигурации.

### Процесс тестирования
1.  **Создание тестов:** При добавлении нового функционала сначала пишите тесты (TDD). Для Python-проектов используйте `pytest`.
2.  **Структура тестов:** Размещайте тесты в папке `tests/` в корне проекта.
3.  **Запуск тестов:** Перед завершением любой задачи убедитесь, что все тесты успешно проходят. Запускайте тесты командой:
    ```bash
    pytest tests/
    ```
4.  **Интеграционное тестирование:** Убедитесь, что компоненты системы (например, фронтенд и бэкенд) корректно взаимодействуют друг с другом в среде Codespaces.

## Технологический Стек

*   **Бэкенд**: Python (Flask)
    *   Парсинг документов: `pdfminer.six`, `python-docx`
    *   Взаимодействие с API: `requests`
    *   Кэширование: Файловая система (JSON)
    *   Шаблонизатор: Jinja2
*   **Фронтенд**: Vanilla JavaScript
*   **AI/LLM**: Универсальный коннектор (DeepSeek/OpenAI)
*   **SEO**: Автоматическая генерация контента и метаданных
*   **Контент**: Markdown с YAML Front Matter
*   **Мониторинг**: Интеграция с внешними API для отслеживания новостей

## Модульная Архитектура

Платформа построена по модульному принципу, где каждый бизнес-сервис является отдельным модулем:

### Модуль 1: Анализ Договоров (`/hababru/`)
- **Цель**: Демонстрация экспертизы в юридтехе
- **Функционал**: AI-анализ договоров, выявление рисков, рекомендации
- **SEO**: Страницы под типы договоров (аренда, поставка, ипотека, etc.)

### Модуль 2: Мониторинг Новостей (`/newsalert/`)
- **Цель**: Демонстрация экспертизы в анализе данных и мониторинге
- **Функционал**: Отслеживание упоминаний, анализ отраслевых новостей
- **SEO**: Страницы под отраслевые темы (ВЭД, логистика, etc.)

### Будущие Модули:
- **Финтех-решения**: Анализ финансовых показателей
- **HR-автоматизация**: Обработка резюме и документооборот
- **Аналитические дашборды**: Визуализация бизнес-метрик

## Центральная SEO-Система

Все модули объединены центральной SEO-системой для максимального покрытия семантического ядра:

## Структура Проекта

```
hababru/
├── .env                      # Переменные окружения (API ключи, токены)
├── .gitignore                # Игнорируемые файлы и директории для Git
├── .pytest_cache/            # Кэш pytest
├── .wakatime-project         # Файл конфигурации Wakatime
├── .wata                     # Вспомогательный файл (возможно, для внутренних нужд)
├── README.md                 # Описание проекта, структура, план работы, инструкции
├── TGStat API.postman_collection.json # Коллекция Postman для работы с TGStat API
├── content/                  # Исходные файлы контента
│   ├── __init__.py           # Инициализация Python-пакета
│   ├── llm_results/          # Результаты работы LLM-промптов
│   │   └── *.txt             # Файлы с результатами LLM-промптов
│   ├── seo_pages/            # Директория для SEO-страниц в формате .md
│   │   ├── __init__.py       # Инициализация Python-пакета
│   │   ├── [slug]/           # Директория для каждой SEO-страницы (например, arendy, dareniya)
│   │   │   ├── example_data.txt # Пример демонстрационных данных для страницы (например, сгенерированный текст договора, новостная сводка)
│   │   │   └── source.md     # Метаданные и основной текст страницы
│   │   └── ...               # Другие SEO-страницы (по одной на каждый ключ)
│   └── seo_prompts/          # Шаблоны промптов для генерации SEO-контента
│       └── *.txt             # Файлы с шаблонами промптов
├── data/                     # Хранилище данных
│   ├── __init__.py           # Инициализация Python-пакета
│   ├── cache/                # Кэш договоров и анализов (например, JSON файлы)
│   │   └── __init__.py       # Инициализация Python-пакета
│   ├── uploads/              # Временно загруженные файлы
│   │   └── __init__.py       # Инициализация Python-пакета
│   └── sample_contracts/     # Примеры договоров
│       ├── __init__.py       # Инициализация Python-пакета
│       └── default_nda.txt   # Пример договора по умолчанию
├── deepseek_api_docs.md      # Документация по DeepSeek API
├── dubna.docx                # Пример DOCX файла (возможно, для тестирования парсинга)
├── public/                   # Статические ресурсы и скомпилированный фронтенд
│   ├── css/                  # Стили CSS
│   │   └── style.css         # Основной файл стилей
│   ├── favicon.ico           # Иконка сайта
│   ├── js/                   # Клиентские скрипты JavaScript
│   │   ├── app.js            # Основная логика фронтенда
│   │   └── seo_admin.js      # Скрипты для страницы администрирования SEO
│   └── robots.txt            # Файл для поисковых роботов
├── pytest.ini                # Конфигурационный файл pytest
├── pytest_output.txt         # Вывод результатов выполнения pytest
├── requirements.txt          # Зависимости Python
├── semantix.txt              # Файл с семантическими запросами (возможно, для SEO)
├── src/                      # Исходный код
│   ├── backend/              # Логика бэкенда (Python)
│   │   ├── __init__.py       # Инициализация Python-пакета
│   │   ├── __pycache__/      # Кэш скомпилированных Python-файлов
│   │   ├── api/              # API эндпоинты
│   │   │   ├── __init__.py   # Инициализация Python-пакета
│   │   │   ├── __pycache__/  # Кэш скомпилированных Python-файлов
│   │   │   └── v1/
│   │   │       ├── __init__.py # Инициализация Python-пакета
│   │   │       ├── __pycache__/ # Кэш скомпилированных Python-файлов
│   │   │       ├── contract_analyzer.py # Эндпоинт для анализа договоров
│   │   │       └── seo_tools.py      # Эндпоинты для администрирования SEO
│   │   ├── cli/              # Скрипты командной строки
│   │   │   ├── __init__.py   # Инициализация Python-пакета
│   │   │   └── generate_seo_page.py # Скрипт для генерации SEO-страниц
│   │   ├── main.py           # Точка входа бэкенд-приложения
│   │   ├── services/         # Бизнес-логика
│   │   │   ├── __init__.py   # Инициализация Python-пакета
│   │   │   ├── __pycache__/  # Кэш скомпилированных Python-файлов
│   │   │   ├── cache_service.py    # Логика кэширования
│   │   │   ├── content_generation_service.py # Сервис для генерации контента
│   │   │   ├── llm_service.py      # Универсальный LLM-коннектор
│   │   │   ├── parsing_service.py  # Парсинг PDF/DOC
│   │   │   ├── seo_prompt_service.py # Сервис для работы с промптами SEO
│   │   │   └── seo_service.py      # Сервис для работы с SEO-страницами
│   │   ├── templates/        # HTML-шаблоны Jinja2
│   │   │   ├── index_template.html # Единый шаблон для всех страниц
│   │   │   └── seo_admin_template.html # Шаблон для страницы администрирования SEO
│   │   └── utils/            # Вспомогательные функции
│   │       └── __init__.py   # Инициализация Python-пакета
│   ├── data/                 # Директория для данных (например, загруженных файлов)
│   │   └── uploads/          # Временно загруженные файлы
│   ├── frontend/             # Исходный код фронтенда
│   │   ├── __init__.py       # Инициализация Python-пакета
│   │   ├── components/       # UI компоненты
│   │   │   └── __init__.py   # Инициализация Python-пакета
│   │   └── services/         # Сервисы фронтенда (вызовы API)
│   │       └── __init__.py   # Инициализация Python-пакета
│   └── shared/               # Общий код для фронтенда и бэкенда
│       └── __init__.py       # Инициализация Python-пакета
├── tests/                    # Автоматизированные тесты
│   ├── test_api.py           # Тесты для API эндпоинтов
│   ├── test_cache_service.py # Тесты для сервиса кэширования
│   ├── test_llm_service.py   # Тесты для LLM-сервиса
│   ├── test_parsing_service.py # Тесты для сервиса парсинга
│   ├── test_seo_admin.py     # Тесты для администрирования SEO
│   ├── test_seo_prompt_api.py # Тесты для API запуска промптов SEO
│   └── test_seo_service.py   # Тесты для SEO-сервиса
└── tree.txt                  # Файл с древовидной структурой проекта
```

## План Работы (Выполнено)

1.  **Инициализация Проекта:**
    *   Создана корневая директория `hababru/`.
    *   Создана базовая структура папок внутри `hababru/`.
    *   Создан файл `hababru/.env` с `DEEPSEEK_API_KEY`, `YANDEX_CLIENT_ID`, `YANDEX_CLIENT_SECRET`, `YANDEX_REDIRECT_URI`.
    *   Создан файл `hababru/README.md` с этим подробным описанием.
    *   Подготовлен файл `data/sample_contracts/default_nda.txt` с примером договора.
    *   Созданы все необходимые `__init__.py` файлы для корректной работы пакетов Python.
    *   Установлены зависимости из `requirements.txt`.

2.  **Разработка Бэкенда (Python с Flask):**
    *   Настроен Flask-фреймворк и реализован `src/backend/main.py` как точка входа.
    *   **Обновлено**: Рефакторинг `src/backend/main.py` для использования функции `create_app()` для инициализации Flask приложения. Это позволяет создавать чистые экземпляры приложения для каждого тестового запуска.
    *   Реализован `src/backend/services/parsing_service.py` для парсинга PDF/DOCX и сегментации текста на пункты/абзацы.
    *   Реализован `src/backend/services/llm_service.py` как универсальный LLM-коннектор, поддерживающий DeepSeek и OpenAI API.
    *   **Обновлено**: Реализован `src/backend/services/cache_service.py` для кэширования результатов анализа и управления статусом асинхронных задач.
    *   **Обновлено**: Реализован `src/backend/api/v1/contract_analyzer.py` с API-эндпоинтами `/upload_contract`, `/start_analysis` (для запуска асинхронного анализа), `/get_analysis_status/<task_id>` (для получения прогресса) и `/get_sample_contract`.
    *   **Обновлено**: Рефакторинг `src/backend/api/v1/seo_tools.py` для использования функции `create_seo_tools_blueprint()`, что позволяет избежать конфликтов при регистрации эндпоинтов в тестах.
    *   Blueprint `contract_analyzer_bp` зарегистрирован в `main.py`.
    *   **Обновлено**: Главная страница и SEO-страницы теперь рендерятся с использованием единого шаблона `src/backend/templates/index_template.html`.

3.  **Разработка Фронтенда (Vanilla JS):**
    *   Статический файл `public/index.html` удален. Главная страница теперь рендерится бэкендом.
    *   Создан `public/css/style.css` для общих стилей.
    *   **Обновлено**: Создан `public/js/app.js` с единой логикой для главной и SEO-страниц:
        *   Добавлен `public/favicon.ico`.
        *   Рандомизация реквизитов примера договора.
        *   Загрузка примера договора через API `/api/v1/get_sample_contract`.
        *   Отображение текста договора по пунктам/абзацам.
        *   Базовая логика для отображения панели анализа при наведении.
        *   Обработчик для загрузки пользовательских файлов и отправки их на анализ.
        *   **Новое**: Реализован асинхронный запуск анализа через `/api/v1/start_analysis`.
        *   **Новое**: Добавлена логика периодического опроса `/api/v1/get_analysis_status/<task_id>` для отображения прогресса анализа (количество обработанных пунктов/абзацев и процент выполнения).
        *   **Новое**: Добавлены элементы UI (текстовое поле и прогресс-бар) для визуализации прогресса.
    *   **Новое**: На главную страницу (теперь через `index_template.html`) добавлен текст о сервисе и ссылки на существующие SEO-страницы договоров.

5.  **Унификация шаблонов и стилей:**
    *   Удален шаблон `src/backend/templates/seo_page_template.html`.
    *   Все страницы теперь используют единый шаблон `src/backend/templates/index_template.html`.
    *   Стили унифицированы в `public/css/style.css`.
    *   JavaScript-логика унифицирована в `public/js/app.js`.

6.  **Тестирование и Отладка:**
    *   Проверена базовая структура проекта и установка зависимостей.
    *   Проверена работа Flask-приложения и обслуживание статических файлов.
    *   Проверена загрузка примера договора через API.
    *   **Обновлено**: Проверена асинхронная работа анализа и отображение прогресса на фронтенде.
    *   **Обновлено**: Автотесты были рефакторингованы для использования `create_app()` и передачи моков сервисов, что решило проблемы с перезаписью эндпоинтов и некорректным мокированием.
    *   **Обновлено**: Исправлена ошибка `TypeError: a bytes-like object is required, not 'str'` в `test_get_sample_contract` путем изменения `read_data` в `mock_open` на байтовую строку.
    *   **Обновлено**: Оптимизировано выполнение `test_seo_page_ipotechnyh_dogovorov_content_display` путем мокирования `analysis_results_raw` с ограниченным количеством пунктов, чтобы избежать долгого анализа.

## Текущий Статус и Последние Обновления

Все файлы проекта, включая бэкенд-сервисы, API-эндпоинты и базовый фронтенд, созданы согласно плану. Асинхронный анализ и отображение прогресса реализованы.

### Крупное обновление (19.07.2025): Добавление всех продуктов на сайт

**Проблема**: На сайте отображалось только 3 продукта из 10+ доступных в папке products.

**Решение**: Исправлены конфигурации всех продуктов в YAML-файлах:

1. **Добавлены недостающие секции в YAML-файлы**:
   - `status: "active"` для всех продуктов
   - `product_class` с правильным указанием модуля и класса
   - Исправлены некорректные `product_id` в нескольких файлах

2. **Исправлены классы продуктов**:
   - Упрощены конструкторы всех продуктов (убраны необязательные параметры)
   - Добавлены недостающие абстрактные методы `get_product_info()` и `get_seo_keywords()`
   - Пересозданы поврежденные файлы `telephony_dashboard.py` и `youtube_telegram_scraper.py`

3. **Исправлены тесты**:
   - Исправлен импорт `product_registry` в тестах
   - Обновлен тест на количество продуктов (теперь проверяет >=2 вместо точного числа)

**Результат**: Теперь на сайте регистрируется **10 продуктов** вместо 3:
- amoexcel_googledrive_sync (Интеграция AMOCRM, Excel и Google Drive)
- bitcoin_mempool_explorer (Bitcoin Mempool Explorer)
- contract_analysis (Анализ договоров с ИИ)
- crm_automation (CRM Автоматизация)
- habab_site_presentations (Презентации сайтов)
- hr_dialogue_mimic (HR Диалог Мимикрия)
- news_analysis (Мониторинг и анализ новостей)
- site_presentations (Презентации сайтов)
- telephony_dashboard (Дашборд телефонии)
- test_ai_tool (Тестовый AI Инструмент)
- youtube_telegram_scraper (YouTube-Telegram Скрапер)

**Тесты**: Все тесты проходят успешно (8/8 passed).

### Обновления по передаче данных на SEO-страницы

*   **Улучшена передача данных на SEO-страницы**: Передача данных `appConfig` из бэкенда на фронтенд для SEO-страниц была переработана для повышения надежности. Теперь данные сериализуются в JSON на стороне Python (`src/backend/services/seo_service.py`) и передаются в скрытый `div` в `src/backend/templates/index_template.html`. Фронтенд (`public/js/app.js`) считывает эти данные из `textContent` этого `div` и парсит их как JSON. Это устраняет проблемы с экранированием символов и обеспечивает корректную инициализацию `window.appConfig`.
*   **Обновлены автотесты**: Соответствующие автотесты (`tests/test_api.py`) были обновлены для проверки нового механизма передачи данных, включая извлечение и парсинг JSON из HTML-ответа.

### Исправленные проблемы

*   **Исправлен `test_get_llm_models`**: Проблема, из-за которой тест `test_get_llm_models` завершался неудачей (возвращал `None` вместо списка моделей), была устранена путем добавления оператора `return unique_models` в конце функции `get_available_models` в `src/backend/services/llm_service.py`.
*   **Удален дублирующийся код в `llm_service.py`**: Из `src/backend/services/llm_service.py` был удален дублирующийся блок кода, что повысило читаемость и поддерживаемость файла.
*   **Исправлен `test_seo_page_content_display`**: Проблема с отображением контента на SEO-страницах, которая приводила к ошибке в `test_seo_page_content_display`, была решена путем изменения логики инициализации `window.appConfig` в `src/backend/templates/index_template.html`. Теперь данные из скрытого `div` парсятся в `window.appConfig` до загрузки `app.js`, что гарантирует их доступность. Также была удалена дублирующая логика парсинга `app-config-data` и дублирующая функция `loadTestContractAndAnalyze` из `public/js/app.js`.

## Новые Возможности (Реализовано)

### 1. Система Продуктов на YAML

Переведена с хардкода на файловую конфигурацию:

- **Структура**: `content/products/` - директория с YAML-файлами продуктов
- **Загрузчик**: `ProductDataLoader` - сервис для загрузки и валидации YAML-конфигов
- **Продукты**: `NewsAnalysisProduct`, `ContractAnalysisProduct` - обновлены для работы с YAML

Пример YAML-конфига:
```yaml
name: "Анализ Договоров"
slug: "contract_analysis"
description: "AI-анализ юридических документов с выявлением рисков"
category: "legaltech"
features:
  - "Автоматический парсинг PDF/DOCX"
  - "AI-анализ каждого пункта"
  - "Выявление потенциальных рисков"
api:
  endpoints:
    - path: "/api/v1/upload_contract"
      method: "POST"
      description: "Загрузка и анализ договора"
```

### 2. Поддержка llms.txt

Реализована генерация машиночитаемого описания платформы согласно спецификации [llmstxt.org](https://llmstxt.org/):

- **Сервис**: `LlmsTxtService` - генерирует структурированное описание
- **Маршрут**: `/llms.txt` - автоматически доступный endpoint
- **Содержимое**: Описание продуктов, API, возможностей платформы

### 3. Telegram Интеграция

Автоматическое создание новых продуктов из сообщений Telegram-канала:

- **TelegramConnector** - подключение к каналу @aideaxondemos
- **TelegramProductGenerator** - генерация YAML-конфигов через LLM
- **TelegramMonitor** - фоновый мониторинг новых сообщений
- **CLI**: `src/backend/cli/telegram_monitor.py` - ручной запуск

#### Настройка Telegram мониторинга:

1. Получите API credentials из [my.telegram.org](https://my.telegram.org)
2. Добавьте в `.env`:
```bash
# Telegram API
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=your_phone
ENABLE_TELEGRAM_MONITORING=true
TELEGRAM_CHECK_INTERVAL=300  # секунды (5 минут)
```

3. Первый запуск (для авторизации):
```bash
cd src/backend/cli
python telegram_monitor.py
```

4. Автоматический мониторинг запускается при старте приложения

#### Как работает:
1. Мониторинг отслеживает новые сообщения в @aideaxondemos
2. LLM анализирует текст и изображения из сообщения  
3. Генерируется YAML-конфиг нового продукта
4. Файл автоматически сохраняется в `content/products/`
5. Продукт становится доступен в системе

### 4. Тестирование

Все новые возможности покрыты автотестами:

- `tests/test_product_data_loader.py` - тесты загрузчика YAML
- `tests/test_llms_txt.py` - тесты генерации llms.txt  
- `tests/test_telegram_product_generator.py` - тесты генерации продуктов
- `tests/test_telegram_connector.py` - тесты Telegram API

Запуск всех тестов:
```bash
pytest tests/ -v
```

## Технологический Стек

*   **Бэкенд**: Python (Flask)
    *   Парсинг документов: `pdfminer.six`, `python-docx`
    *   Взаимодействие с API: `requests`
    *   Кэширование: Файловая система (JSON)
    *   Шаблонизатор: Jinja2
*   **Фронтенд**: Vanilla JavaScript
*   **AI/LLM**: Универсальный коннектор (DeepSeek/OpenAI)
*   **SEO**: Автоматическая генерация контента и метаданных
*   **Контент**: Markdown с YAML Front Matter
*   **Мониторинг**: Интеграция с внешними API для отслеживания новостей

## Обновления и Исправления

### 1. Удаление `/demo/` из ссылок на продукты
- **Файл**: `hababru/public/js/app.js`
- **Изменение**: Удален префикс `/demo/` из URL-адресов продуктов, чтобы ссылки вели напрямую к страницам продуктов (например, `/product_id` вместо `/demo/product_id`).

### 2. Объяснение значения `other` в категориях продуктов
- В файле `hababru/src/backend/api/v1/seo_tools.py` (функция `get_existing_products`) и `hababru/src/backend/main.py` (функция `get_products_list`) значение `'other'` используется как категория по умолчанию для продуктов, у которых явно не указана категория в их конфигурации. Это позволяет классифицировать продукты, не имеющие специфической категории.

### 3. Исправление ошибок 404 в админке
- **Проблема**: Запросы к API `/api/v1/seo_pages_list` и `/api/v1/products/stats` возвращали ошибку 404.
- **Причина**: Blueprint `seo_tools` был зарегистрирован в `main.py` с префиксом `/admin`, что означало, что все его эндпоинты должны были вызываться с `/admin/` в начале пути (например, `/admin/seo_pages_list`). Фронтенд же продолжал использовать старые пути (`/api/v1/`).
- **Исправление**:
    - **Файл**: `hababru/public/js/seo_admin.js`
    - **Изменение**: Обновлены пути запросов к `/admin/seo_pages_list` и `/admin/get_llm_models`.
    - **Файл**: `hababru/src/backend/templates/admin/dashboard.html`
    - **Изменение**: Обновлены пути запросов к `/admin/seo_pages_list` и `/admin/products/stats`.

### 4. Проблема с таймаутом LLM-сервиса
- **Проблема**: Тест `tests/test_arendy_page.py` завершается с ошибкой `Timeout` во время вызова `llm_service.analyze_paragraph_in_context`.
- **Анализ**: Это указывает на то, что LLM-сервис не отвечает в течение установленного времени. Причины могут быть различными: высокая нагрузка на LLM API, проблемы с сетью, или слишком сложный запрос, требующий больше времени для обработки.
- **Предпринятые действия**:
    - **Файл**: `hababru/src/backend/services/llm_service.py`
    - **Изменение**: Увеличен таймаут для `generate_text` до 300 секунд и для `analyze_paragraph_in_context` до 600 секунд.
    - **Изменение**: Исправлена опечатка в названии модели `gpt-3.5-тurbo` в функции `_get_openai_models`.
- **Статус**: Несмотря на увеличение таймаутов, проблема сохраняется. Это указывает на то, что проблема, вероятно, находится вне контроля приложения (например, в доступности внешнего LLM API). Для дальнейшего решения этой проблемы потребуется дополнительная диагностика внешнего LLM API или рассмотрение альтернативных LLM-провайдеров/моделей.

### 5. Добавление простейшего сборщика логов из браузера
- **Функционал**: Реализован механизм для сбора ошибок JavaScript из браузера и их сохранения в файл на сервере.
- **Реализация**:
    - **Бэкенд**: Создан новый Blueprint `browser_log_bp` в `hababru/src/backend/api/v1/browser_log.py` с эндпоинтом `/log_browser_error`. Этот Blueprint зарегистрирован в `hababru/src/backend/main.py` с префиксом `/api/v1/`, делая его общедоступным. Старый эндпоинт из `hababru/src/backend/api/v1/seo_tools.py` удален. В эндпоинт `log_browser_error` добавлено дополнительное логирование для отладки.
    - **Фронтенд**: В `hababru/public/js/app.js` глобальный обработчик `window.onerror` был перемещен за пределы `DOMContentLoaded` и других функций, чтобы гарантировать его однократную и корректную регистрацию. Он перехватывает необработанные ошибки JavaScript и отправляет их на новый общедоступный бэкенд-эндпоинт `/api/v1/log_browser_error`. В `hababru/src/backend/templates/admin/base.html` также добавлен глобальный обработчик `window.onerror` для страниц админки.
    - **Тестовая кнопка**: В `hababru/src/backend/templates/index_template.html` добавлена кнопка "Вызвать тестовую ошибку", которая при нажатии намеренно вызывает ошибку JavaScript, чтобы проверить работу сборщика логов.
- **Файл логов**: Ошибки браузера будут записываться в `hababru/logs/browser.log`.

## Рекомендации для дальнейшей работы

- **Доступ к админке на продакшене**: На продакшене доступ к `/admin` закрыт формой логина. Это означает, что все API-эндпоинты, предназначенные для использования на публичной части сайта, должны быть вынесены из Blueprint'а `/admin` в общедоступные Blueprint'ы (например, `/api/v1/`), как это было сделано для сборщика логов браузера.
- **Диагностика LLM-сервиса**: Если проблема с таймаутом LLM-сервиса сохраняется, рекомендуется провести более глубокую диагностику доступности и производительности используемых LLM API (DeepSeek, OpenAI). Возможно, потребуется связаться с поддержкой провайдера или рассмотреть использование локальных LLM-моделей для тестирования.
- **Мониторинг логов**: Включить более детальное логирование запросов к LLM API для выявления конкретных причин таймаутов (например, статус-коды ответов, время ответа).
- **Оптимизация промптов**: Проверить промпты, используемые для анализа, на предмет их сложности. Возможно, их можно упростить, чтобы сократить время ответа LLM.
- **Обработка ошибок LLM**: Улучшить обработку ошибок LLM-сервиса, чтобы приложение могло корректно реагировать на таймауты и другие проблемы, не приводя к полному сбою.
- **Просмотр логов браузера**: Регулярно проверять файл `hababru/logs/browser.log` для выявления и устранения ошибок на стороне клиента.

## Система Продуктов

### Архитектура продуктов
Платформа использует модульную архитектуру для управления продуктами. Каждый продукт представлен отдельным YAML-файлом конфигурации и соответствующим Python-классом.

### Структура продукта
```
/content/products/
├── _template.yaml                 # Шаблон для новых продуктов
├── contract_analysis.yaml        # Конфигурация анализа договоров
├── news_analysis.yaml           # Конфигурация мониторинга новостей
└── other_products.yaml          # Другие продукты
```

### Создание нового продукта

#### Шаг 1: Создайте YAML конфигурацию
1. Скопируйте `/content/products/_template.yaml`
2. Переименуйте в `/content/products/your_product_id.yaml`
3. Заполните конфигурацию:

```yaml
---
product_id: "unique_product_id"    # Уникальный идентификатор
name: "Название продукта"          # Человекочитаемое название
description: "Описание продукта"   # Краткое описание функционала
version: "1.0"                     # Версия продукта
category: "category_name"          # Категория (legal, analytics, automation, etc.)
status: "active"                   # Статус: active, inactive, development

# Конфигурация класса продукта
product_class:
  module: "hababru.src.backend.services.products.your_product"
  class_name: "YourProductClass"
  dependencies:
    - "llm_service"
    # Дополнительные зависимости по необходимости

# Демо-данные для отображения на странице продукта
demo_data:
  key_features:
    - "Основная функция 1"
    - "Основная функция 2"
  target_audience:
    - "Целевая аудитория 1"
    - "Целевая аудитория 2"
  use_cases:
    - "Сценарий использования 1"
    - "Сценарий использования 2"

# Информация о продукте для SEO
product_info:
  key_benefits:
    - "Преимущество 1"
    - "Преимущество 2"
  target_audience:
    - "Бизнес-аудитория 1"
    - "Бизнес-аудитория 2"
```

#### Шаг 2: Создайте класс продукта
Создайте файл `/src/backend/services/products/your_product.py`:

```python
from ..products import BaseProduct
from ..llm_service import LLMService
from ..product_data_loader import ProductDataLoader

class YourProductClass(BaseProduct):
    def __init__(self, llm_service: LLMService):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("your_product_id")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        self.llm_service = llm_service
    
    def get_demo_content(self):
        """Возвращает демо-контент для отображения на странице"""
        return self.product_data.get("demo_data", {})
    
    def execute_demo(self, demo_params):
        """Выполняет демо-версию продукта"""
        # Реализуйте логику демо-выполнения
        return {"status": "demo_executed", "result": "demo_result"}
```

#### Шаг 3: Регистрация продукта (автоматическая)
Система автоматически обнаружит и зарегистрирует новый продукт при запуске, если:
- YAML файл корректно заполнен
- Класс продукта существует и доступен для импорта
- Статус продукта установлен в "active"

### Создание SEO страниц для продукта

#### Шаг 1: Создайте директорию SEO страницы
```bash
mkdir /content/seo_pages/your-seo-page-slug
```

#### Шаг 2: Создайте source.md файл
Создайте `/content/seo_pages/your-seo-page-slug/source.md`:

```markdown
---
title: "SEO заголовок страницы"
meta_description: "Описание для поисковиков"
meta_keywords:
  - "ключевое слово 1"
  - "ключевое слово 2"
  - "ключевое слово 3"
main_keyword: "основное ключевое слово"
related_keywords:
  - "связанное ключевое слово 1"
  - "связанное ключевое слово 2"
product_id: "your_product_id"     # ID продукта, к которому относится страница
created_at: 2025-07-19
---

# Заголовок SEO страницы

Основной контент SEO страницы в Markdown формате.

## Подзаголовок

- Список преимуществ
- Описание функциональности
- Целевая аудитория

**Призыв к действию**
```

#### Шаг 3: Зарегистрируйте связь SEO страницы с продуктом
В файле `/src/backend/main.py` добавьте связь:

```python
# Регистрируем связи между продуктами и SEO-страницами
try:
    # Связываем ваш продукт с SEO-страницами
    product_registry.map_seo_page_to_product('your-seo-page-slug', 'your_product_id')
    app.logger.info("Зарегистрированы связи между продуктами и SEO-страницами")
except Exception as e:
    app.logger.warning(f"Ошибка при регистрации связей продуктов с SEO-страницами: {e}")
```

#### Шаг 4: Перезапустите приложение
После добавления SEO страниц перезапустите приложение, чтобы они стали доступны.

### Доступные типы зависимостей для продуктов:
- `llm_service` - Сервис для работы с LLM
- `parsing_service` - Сервис парсинга документов  
- `cache_service` - Сервис кэширования

### Категории продуктов:
- `legal` - Юридические продукты
- `analytics` - Аналитические продукты
- `automation` - Автоматизация процессов
- `finance` - Финансовые продукты
- `other` - Прочие продукты

### Автоматическая регистрация
Система автоматически обнаруживает и регистрирует все активные продукты при запуске. Используется `ProductFactory` для динамического создания экземпляров продуктов на основе их YAML конфигурации.

### Тестирование и отладка

#### Проверка конфигурации продукта:
```bash
# Валидация YAML файла
python -c "import yaml; print(yaml.safe_load(open('content/products/your_product.yaml')))"

# Проверка загрузки продукта
python debug_llms.py
```

#### Проверка регистрации:
После запуска приложения проверьте логи на наличие:
```
Зарегистрирован продукт: your_product_id
```

#### Тестирование SEO страниц:
1. Откройте `/seo-page-slug` для просмотра отдельной SEO страницы
2. Откройте `/products/your_product_id` для просмотра страницы продукта
3. Убедитесь, что SEO ссылки отображаются в разделе "Полезные ссылки"

### Часто встречающиеся ошибки:

1. **"Продукт не найден для ID"** - Проверьте правильность product_id в YAML файле
2. **"Ошибка создания продукта: отсутствует конфигурация product_class"** - Убедитесь, что секция product_class заполнена
3. **"ModuleNotFoundError"** - Проверьте правильность пути к модулю в product_class.module
4. **SEO ссылки не отображаются** - Проверьте регистрацию связей в main.py

### Динамическая загрузка
- Продукты загружаются из YAML файлов
- Классы импортируются динамически
- Зависимости внедряются автоматически
- SEO страницы и демо примеры настраиваются декларативно

---

## Быстрое Добавление Новых Продуктов

Основываясь на опыте реализации продукта "Создание Презентационных Сайтов", ниже приведена пошаговая инструкция для быстрого добавления новых продуктов в платформу.

### Рекомендуемый Порядок Разработки

#### 1. Создание и Запуск Тестов (TDD Подход)
**Время: ~15 минут**

Начните с создания файла тестов в `/tests/test_[product_name]_product.py`:

```python
import pytest
from unittest.mock import Mock, patch
from src.backend.services.products.[product_name] import [ProductClass]
from src.backend.services.llm_service import LLMService

class Test[ProductClass]:
    @pytest.fixture
    def mock_llm_service(self):
        mock = Mock(spec=LLMService)
        mock.generate_text.return_value = "mock response"
        return mock
    
    @pytest.fixture
    def product(self, mock_llm_service):
        return [ProductClass](mock_llm_service)
    
    def test_product_initialization(self, product):
        assert product.product_id == "[product_id]"
        assert product.name == "[Product Name]"
    
    def test_execute_demo(self, product):
        result = product.execute_demo({})
        assert "status" in result
        
    # Добавьте тесты для всех основных методов
```

Запустите тесты (они должны упасть):
```bash
pytest tests/test_[product_name]_product.py -v
```

#### 2. Создание YAML Конфигурации
**Время: ~10 минут**

Создайте файл `/content/products/[product_id].yaml`:

```yaml
---
product_id: "[unique_product_id]"
name: "[Product Display Name]"
description: "[Brief product description]"
version: "1.0"
category: "[appropriate_category]"
status: "active"

product_class:
  module: "src.backend.services.products.[product_name]"
  class_name: "[ProductClass]"
  dependencies:
    - "llm_service"
    - "parsing_service"  # при необходимости
    - "cache_service"    # при необходимости

# Интерфейсы для формы на фронтенде
interfaces:
  input:
    title: "Загрузка Данных"
    fields:
      - name: "main_file"
        type: "file"
        label: "Основной файл"
        accept: ".pdf,.doc,.docx"
        required: true
      - name: "additional_info"
        type: "text"
        label: "Дополнительная информация"
        placeholder: "Введите дополнительные данные"
        required: false
  
  output:
    title: "Результат Обработки"
    format: "html"  # или "json", "text"

# Демо-данные для страницы продукта
demo_data:
  sample_input: "Пример входных данных"
  sample_output: "Пример результата"
  key_features:
    - "Основная функция 1"
    - "Основная функция 2"
    - "Основная функция 3"

# SEO информация
seo:
  meta_title: "[SEO заголовок]"
  meta_description: "[SEO описание для поисковиков]"
  keywords:
    - "ключевое слово 1"
    - "ключевое слово 2"
  main_keyword: "главное ключевое слово"
```

#### 3. Реализация Класса Продукта
**Время: ~30 минут**

Создайте файл `/src/backend/services/products/[product_name].py`:

```python
import os
import json
from typing import Dict, Any, Optional
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
from ..product_data_loader import ProductDataLoader

class [ProductClass](BaseProduct):
    def __init__(self, llm_service: LLMService, parsing_service: ParsingService = None, cache_service: CacheService = None):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("[product_id]")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        
        self.llm_service = llm_service
        self.parsing_service = parsing_service
        self.cache_service = cache_service
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Возвращает демо-контент для отображения на странице"""
        return self.product_data.get("demo_data", {})
    
    def execute_demo(self, demo_params: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполняет демо-версию продукта"""
        try:
            # Логика демо-выполнения
            demo_result = self._process_demo_data()
            
            return {
                "status": "success",
                "result": demo_result,
                "demo": True
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "demo": True
            }
    
    def process_upload(self, files: Dict, form_data: Dict) -> Dict[str, Any]:
        """Обрабатывает загруженные файлы и данные формы"""
        try:
            # Основная логика обработки
            result = self._process_user_data(files, form_data)
            
            return {
                "status": "success",
                "result": result,
                "demo": False
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "demo": False
            }
    
    def _process_demo_data(self) -> str:
        """Внутренний метод для обработки демо-данных"""
        demo_input = self.product_data.get("demo_data", {}).get("sample_input", "")
        
        # Используйте LLM для генерации демо-результата
        prompt = f"Обработайте следующие данные: {demo_input}"
        return self.llm_service.generate_text(prompt)
    
    def _process_user_data(self, files: Dict, form_data: Dict) -> str:
        """Внутренний метод для обработки пользовательских данных"""
        # Обработка файлов при необходимости
        if self.parsing_service and files:
            parsed_content = self._parse_uploaded_files(files)
        else:
            parsed_content = ""
        
        # Подготовка данных для LLM
        combined_data = f"Файлы: {parsed_content}
Дополнительно: {form_data.get('additional_info', '')}"
        
        # Генерация результата через LLM
        prompt = f"Обработайте следующие данные: {combined_data}"
        return self.llm_service.generate_text(prompt)
    
    def _parse_uploaded_files(self, files: Dict) -> str:
        """Парсинг загруженных файлов"""
        if not self.parsing_service:
            return ""
        
        parsed_content = []
        for field_name, file_list in files.items():
            for file_obj in file_list:
                if hasattr(file_obj, 'filename') and file_obj.filename:
                    content = self.parsing_service.parse_document(file_obj)
                    parsed_content.append(content)
        
        return "

".join(parsed_content)
```

#### 4. Создание API Endpoints
**Время: ~20 минут**

Создайте файл `/src/backend/api/v1/[product_name].py`:

```python
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from typing import Dict, Any

def create_[product_name]_blueprint():
    """Создает Blueprint для API продукта"""
    bp = Blueprint('[product_name]', __name__)
    
    @bp.route('/[product_name]/info', methods=['GET'])
    def get_product_info():
        """Получение информации о продукте"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('[product_id]')
            demo_content = product.get_demo_content()
            
            return jsonify({
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "demo_content": demo_content
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/[product_name]/demo', methods=['POST'])
    def execute_demo():
        """Выполнение демо-версии продукта"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            product = product_factory.create_product('[product_id]')
            demo_params = request.get_json() or {}
            result = product.execute_demo(demo_params)
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e), "status": "error"}), 500
    
    @bp.route('/[product_name]/create', methods=['POST'])
    def process_upload():
        """Обработка загруженных файлов"""
        try:
            product_factory = current_app.config.get('PRODUCT_FACTORY')
            if not product_factory:
                return jsonify({"error": "Product factory not available"}), 500
            
            # Получение файлов и данных формы
            files = {}
            for field_name in request.files:
                files[field_name] = request.files.getlist(field_name)
            
            form_data = request.form.to_dict()
            
            product = product_factory.create_product('[product_id]')
            result = product.process_upload(files, form_data)
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e), "status": "error"}), 500
    
    return bp

# Экспорт для использования в main.py
[product_name]_bp = create_[product_name]_blueprint()
```

#### 5. Регистрация API в Главном Приложении
**Время: ~5 минут**

В файле `/src/backend/main.py` добавьте:

```python
# В секции импортов
from .api.v1.[product_name] import [product_name]_bp

# В функции create_app, после создания app:
app.register_blueprint([product_name]_bp, url_prefix='/api/v1')
```

#### 6. Добавление Формы на Фронтенд
**Время: ~25 минут**

В файле `/src/backend/templates/index_template.html` найдите секцию условий для продуктов и добавьте:

```html
{% elif page_data.product_id == '[product_id]' %}
<div class="upload-section">
    <h2>{{ product_info.interfaces.input.title }}</h2>
    <form id="[product_name]Form" enctype="multipart/form-data">
        {% for field in product_info.interfaces.input.fields %}
        <div class="form-group">
            <label for="{{ field.name }}">{{ field.label }}{% if field.required %} *{% endif %}</label>
            {% if field.type == 'file' %}
            <input type="file" 
                   id="{{ field.name }}" 
                   name="{{ field.name }}" 
                   accept="{{ field.accept }}" 
                   {% if field.required %}required{% endif %}
                   multiple>
            {% elif field.type == 'text' %}
            <input type="text" 
                   id="{{ field.name }}" 
                   name="{{ field.name }}" 
                   placeholder="{{ field.placeholder or '' }}" 
                   {% if field.required %}required{% endif %}>
            {% endif %}
        </div>
        {% endfor %}
        
        <button type="submit" class="btn-primary">Обработать</button>
        <button type="button" class="btn-secondary" onclick="execute[ProductClass]Demo()">Демо</button>
    </form>
    
    <div class="progress-container" id="[product_name]Progress" style="display: none;">
        <div class="progress-text">Обработка данных...</div>
        <div class="progress-bar">
            <div class="progress-fill" id="[product_name]ProgressFill"></div>
        </div>
    </div>
    
    <div class="result-container" id="[product_name]Result" style="display: none;">
        <h3>{{ product_info.interfaces.output.title }}</h3>
        <div class="result-content" id="[product_name]ResultContent"></div>
    </div>
</div>
```

#### 7. Добавление JavaScript Обработчиков
**Время: ~20 минут**

В файле `/public/js/app.js` добавьте:

```javascript
// В секции обработчиков DOMContentLoaded
if (appConfig.productId === '[product_id]') {
    const form = document.getElementById('[product_name]Form');
    if (form) {
        form.addEventListener('submit', handle[ProductClass]Submit);
    }
}

// Функция обработки отправки формы
async function handle[ProductClass]Submit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Показываем прогресс
    showProgress('[product_name]Progress', '[product_name]ProgressFill');
    hideElement('[product_name]Result');
    
    try {
        const response = await fetch('/api/v1/[product_name]/create', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        hideProgress('[product_name]Progress');
        showResult('[product_name]Result', '[product_name]ResultContent', result);
        
    } catch (error) {
        console.error('Ошибка при обработке:', error);
        hideProgress('[product_name]Progress');
        showError('[product_name]Result', '[product_name]ResultContent', 'Произошла ошибка при обработке данных');
        logErrorToBrowser('Handle[ProductClass]Submit Error', error.message, window.location.href);
    }
}

// Функция демо
async function execute[ProductClass]Demo() {
    showProgress('[product_name]Progress', '[product_name]ProgressFill');
    hideElement('[product_name]Result');
    
    try {
        const response = await fetch('/api/v1/[product_name]/demo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        });
        
        const result = await response.json();
        
        hideProgress('[product_name]Progress');
        showResult('[product_name]Result', '[product_name]ResultContent', result);
        
    } catch (error) {
        console.error('Ошибка при выполнении демо:', error);
        hideProgress('[product_name]Progress');
        showError('[product_name]Result', '[product_name]ResultContent', 'Произошла ошибка при выполнении демо');
        logErrorToBrowser('Execute[ProductClass]Demo Error', error.message, window.location.href);
    }
}
```

#### 8. Обновление и Проверка Тестов
**Время: ~10 минут**

Запустите тесты и убедитесь, что все проходят:

```bash
pytest tests/test_[product_name]_product.py -v
```

Если тесты не проходят, исправьте ошибки в коде продукта.

#### 9. Проверка Интеграции
**Время: ~15 минут**

1. Запустите приложение:
```bash
python -m src.backend.main
```

2. Проверьте доступность эндпоинтов:
   - `GET /api/v1/[product_name]/info`
   - `POST /api/v1/[product_name]/demo`
   - `POST /api/v1/[product_name]/create`

3. Откройте страницу продукта: `/products/[product_id]`

4. Протестируйте форму и демо-функционал

### Общие Рекомендации

**Соглашения об именовании:**
- Файлы и директории: `snake_case`
- Классы: `PascalCase`
- Переменные и функции: `snake_case`
- YAML ключи: `snake_case`

**Обработка ошибок:**
- Всегда используйте try/except блоки
- Возвращайте структурированные ответы с полем "status"
- Логируйте ошибки для отладки

**Тестирование:**
- Начинайте с TDD подхода
- Мокируйте внешние зависимости
- Покрывайте все основные сценарии использования

**Производительность:**
- Используйте кэширование для повторяющихся операций
- Оптимизируйте промпты для LLM
- Ограничивайте размер загружаемых файлов

### Время Разработки

При следовании данной инструкции общее время разработки нового продукта составляет **~2-3 часа**:

- Тесты: 15 мин
- YAML конфиг: 10 мин  
- Класс продукта: 30 мин
- API endpoints: 20 мин
- Регистрация: 5 мин
- Фронтенд форма: 25 мин
- JavaScript: 20 мин
- Проверка тестов: 10 мин
- Интеграционное тестирование: 15 мин

**Итого: ~150 минут (2.5 часа)**

### Частые Ошибки и Решения

1. **ProductFactory not available** - Убедитесь, что продукт зарегистрирован в main.py
2. **Модуль не найден** - Проверьте правильность пути в YAML конфигурации
3. **Тесты не проходят** - Убедитесь, что все зависимости правильно замоканы
4. **Форма не отправляется** - Проверьте правильность product_id в условиях шаблона
5. **404 на API эндпоинтах** - Убедитесь, что Blueprint зарегистрирован в main.py

````
