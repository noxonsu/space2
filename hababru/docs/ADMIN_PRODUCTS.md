# Руководство по добавлению новых продуктов в HababRu

## Обзор системы

HababRu использует YAML-файлы для конфигурации продуктов. Каждый продукт представлен отдельным YAML-файлом в директории `/content/products/`. Система автоматически загружает все активные продукты и создает для них соответствующие экземпляры классов.

## Структура YAML файла продукта

Каждый файл продукта должен следовать стандартной структуре. Используйте `_template.yaml` как основу:

### Обязательные поля

```yaml
# Метаданные продукта
product_id: "unique_product_id"    # Уникальный идентификатор
name: "Название продукта"          # Человекочитаемое название
description: "Описание продукта"   # Краткое описание функционала
version: "1.0"                     # Версия продукта
category: "category_name"          # Категория (legal, analytics, automation, etc.)
status: "active"                   # Статус: active, inactive, development

# Конфигурация класса продукта
product_class:
  module: "hababru.src.backend.services.products.product_module"
  class_name: "ProductClassName"
  dependencies:                    # Список требуемых сервисов
    - "llm_service"
    # Дополнительные зависимости по необходимости
```

### Дополнительные секции

```yaml
# Демо-данные для отображения на странице продукта
demo_data:
  key_features: []
  target_audience: []
  use_cases: []

# SEO страницы, связанные с продуктом
seo_pages:
  - path: "seo-url"
    title: "SEO заголовок"
    description: "SEO описание"
    category: "category_name"

# Демо примеры продукта
demo_examples:
  - path: "demo-url"
    title: "Демо заголовок"
    description: "Демо описание"
```

## Пошаговое добавление нового продукта

### Шаг 1: Создание класса продукта

1. Создайте новый файл в `/src/backend/services/products/your_product.py`
2. Наследуйте класс от `BaseProduct`
3. Реализуйте необходимые методы

Пример:
```python
from ..products import BaseProduct
from ..llm_service import LLMService
from ..product_data_loader import ProductDataLoader

class YourProduct(BaseProduct):
    def __init__(self, llm_service: LLMService):
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("your_product_id")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        self.llm_service = llm_service
```

### Шаг 2: Создание YAML конфигурации

1. Скопируйте `/content/products/_template.yaml`
2. Переименуйте в `/content/products/your_product_id.yaml`
3. Заполните все необходимые поля

### Шаг 3: Автоматическая регистрация

Система автоматически обнаружит и зарегистрирует новый продукт при следующем запуске, если:
- YAML файл корректно заполнен
- Класс продукта существует и доступен для импорта
- Статус продукта установлен в "active"

## Типы зависимостей

### Доступные сервисы:
- `llm_service` - Сервис для работы с LLM
- `parsing_service` - Сервис парсинга документов
- `cache_service` - Сервис кэширования
- Другие сервисы можно добавить в `ProductFactory`

### Конфигурация зависимостей:
```yaml
product_class:
  dependencies:
    - "llm_service"           # Только LLM
    - "parsing_service"       # + Парсинг документов
    - "cache_service"         # + Кэширование
```

## SEO конфигурация

### SEO страницы
Каждый продукт может иметь связанные SEO страницы:

```yaml
seo_pages:
  - path: "contract-analysis"
    title: "Анализ договоров с ИИ"
    description: "Профессиональный анализ юридических документов"
    category: "legal"
  - path: "legal-consulting"
    title: "Юридическое консультирование"
    description: "ИИ-помощник для юристов"
    category: "legal"
```

### Демо примеры
```yaml
demo_examples:
  - path: "product_demo"
    title: "Интерактивное демо"
    description: "Попробуйте продукт в действии"
  - path: "api/sample-data"
    title: "Примеры API"
    description: "Тестовые данные для API"
```

## Отладка и тестирование

### Проверка конфигурации
```bash
# Валидация YAML
python -c "import yaml; yaml.safe_load(open('content/products/your_product.yaml'))"

# Тест загрузки продукта
python debug_llms.py
```

### Проверка регистрации
После запуска приложения проверьте логи на наличие:
```
Зарегистрирован продукт: your_product_id
```

## Статусы продуктов

- `active` - Продукт активен и доступен
- `inactive` - Продукт временно отключен
- `development` - Продукт в разработке

## Категории продуктов

- `legal` - Юридические продукты
- `analytics` - Аналитические продукты  
- `automation` - Автоматизация процессов
- `finance` - Финансовые продукты
- `other` - Прочие продукты

## Часто встречающиеся ошибки

1. **Неверный module path** - Убедитесь, что путь к модулю корректен
2. **Отсутствующие зависимости** - Проверьте, что все сервисы зарегистрированы
3. **Неверная структура YAML** - Используйте YAML валидатор
4. **Дублирующиеся product_id** - Каждый ID должен быть уникальным

## Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь в корректности YAML структуры
3. Проверьте доступность класса продукта
4. Используйте `debug_llms.py` для тестирования
