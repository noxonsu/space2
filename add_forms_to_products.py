#!/usr/bin/env python3
"""
Скрипт для добавления форм во все продукты, которые их не имеют
"""

import sys
import os
import yaml
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hababru'))

from hababru.src.backend.services.product_data_loader import ProductDataLoader


def get_products_needing_forms():
    """Находит продукты, которым нужны формы"""
    data_loader = ProductDataLoader()
    available_products = data_loader.get_available_products()
    
    products_needing_forms = []
    
    for product_id in available_products:
        if product_id == '_template':  # Пропускаем шаблон
            continue
            
        try:
            product_data = data_loader.load_product_data(product_id)
            interfaces = product_data.get('interfaces', {})
            input_interface = interfaces.get('input', {})
            
            # Проверяем, нужна ли форма
            needs_form = False
            if not input_interface:
                needs_form = True
                reason = "Нет интерфейса ввода"
            elif not input_interface.get('properties'):
                needs_form = True
                reason = "Пустой интерфейс ввода"
            else:
                reason = "Форма уже есть"
            
            products_needing_forms.append({
                'id': product_id,
                'name': product_data.get('name', 'Без названия'),
                'category': product_data.get('category', 'unknown'),
                'needs_form': needs_form,
                'reason': reason,
                'file_path': Path('hababru/content/products') / f"{product_id}.yaml"
            })
            
        except Exception as e:
            print(f"❌ Ошибка анализа {product_id}: {e}")
    
    return products_needing_forms


def create_form_for_product(product_info):
    """Создает подходящую форму для продукта на основе его категории и назначения"""
    
    category = product_info['category'].lower()
    product_id = product_info['id']
    name = product_info['name']
    
    # Определяем форму на основе категории и названия
    if 'crm' in product_id.lower() or 'crm' in name.lower():
        return {
            'input': {
                'type': 'object',
                'properties': {
                    'entity_type': {
                        'type': 'string',
                        'description': 'Тип сущности для автоматизации (лид, сделка, контакт)',
                        'example': 'лид',
                        'enum': ['лид', 'сделка', 'контакт', 'задача']
                    },
                    'action': {
                        'type': 'string', 
                        'description': 'Действие для выполнения',
                        'example': 'создать',
                        'enum': ['создать', 'обновить', 'удалить', 'получить']
                    },
                    'data': {
                        'type': 'string',
                        'description': 'Данные для обработки в формате JSON',
                        'example': '{"name": "Иван Иванов", "phone": "+7999..."}'
                    }
                },
                'required': ['entity_type', 'action']
            },
            'output': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'description': 'Статус выполнения операции'
                    },
                    'result': {
                        'type': 'object',
                        'description': 'Результат операции'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'Сообщение о результате'
                    }
                }
            }
        }
        
    elif 'site' in product_id.lower() or 'presentation' in product_id.lower():
        return {
            'input': {
                'type': 'object',
                'properties': {
                    'company_name': {
                        'type': 'string',
                        'description': 'Название компании для сайта',
                        'example': 'ООО "Технологии будущего"'
                    },
                    'business_type': {
                        'type': 'string',
                        'description': 'Тип бизнеса',
                        'example': 'IT-консалтинг',
                        'enum': ['IT-услуги', 'Производство', 'Торговля', 'Консалтинг', 'Финансы', 'Образование']
                    },
                    'target_audience': {
                        'type': 'string',
                        'description': 'Целевая аудитория',
                        'example': 'B2B клиенты, средний и крупный бизнес'
                    },
                    'key_services': {
                        'type': 'string',
                        'description': 'Ключевые услуги (через запятую)',
                        'example': 'Разработка ПО, Консалтинг, Техподдержка'
                    }
                },
                'required': ['company_name', 'business_type']
            },
            'output': {
                'type': 'object',
                'properties': {
                    'website_structure': {
                        'type': 'object',
                        'description': 'Структура сайта с разделами и контентом'
                    },
                    'generated_content': {
                        'type': 'array',
                        'description': 'Сгенерированный контент для страниц'
                    },
                    'design_recommendations': {
                        'type': 'array',
                        'description': 'Рекомендации по дизайну'
                    }
                }
            }
        }
        
    elif 'test' in product_id.lower() or category == 'ai':
        return {
            'input': {
                'type': 'object',
                'properties': {
                    'test_query': {
                        'type': 'string',
                        'description': 'Тестовый запрос для AI инструмента',
                        'example': 'Проанализируй эффективность маркетинговой кампании'
                    },
                    'parameters': {
                        'type': 'object',
                        'description': 'Дополнительные параметры для анализа',
                        'properties': {
                            'model': {
                                'type': 'string',
                                'description': 'Модель AI для использования',
                                'example': 'gpt-4'
                            },
                            'temperature': {
                                'type': 'number',
                                'description': 'Температура генерации (0-1)',
                                'example': 0.7
                            }
                        }
                    }
                },
                'required': ['test_query']
            },
            'output': {
                'type': 'object',
                'properties': {
                    'ai_response': {
                        'type': 'string',
                        'description': 'Ответ AI системы'
                    },
                    'analysis_metrics': {
                        'type': 'object',
                        'description': 'Метрики анализа'
                    },
                    'recommendations': {
                        'type': 'array',
                        'description': 'Рекомендации на основе анализа'
                    }
                }
            }
        }
        
    else:
        # Универсальная форма для остальных продуктов
        return {
            'input': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': f'Запрос для {name}',
                        'example': 'Пример запроса'
                    },
                    'options': {
                        'type': 'object',
                        'description': 'Дополнительные параметры',
                        'properties': {
                            'format': {
                                'type': 'string',
                                'description': 'Формат ответа',
                                'example': 'json'
                            }
                        }
                    }
                },
                'required': ['query']
            },
            'output': {
                'type': 'object',
                'properties': {
                    'result': {
                        'type': 'string',
                        'description': 'Результат обработки запроса'
                    },
                    'metadata': {
                        'type': 'object',
                        'description': 'Метаданные результата'
                    }
                }
            }
        }


def update_product_file(product_info, new_interfaces):
    """Обновляет файл продукта, добавляя интерфейсы"""
    
    file_path = Path('/workspaces/space2') / product_info['file_path']
    
    try:
        # Читаем существующий файл
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Парсим YAML
        data = yaml.safe_load(content)
        
        # Добавляем или обновляем интерфейсы
        data['interfaces'] = new_interfaces
        
        # Сохраняем обратно
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ Обновлен файл: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления {file_path}: {e}")
        return False


def main():
    print("=== ДОБАВЛЕНИЕ ФОРМ ВО ВСЕ ПРОДУКТЫ ===\n")
    
    # Находим продукты, которым нужны формы
    products = get_products_needing_forms()
    
    print("📋 АНАЛИЗ ПРОДУКТОВ:")
    products_to_update = []
    
    for product in products:
        print(f"📦 {product['name']} ({product['id']})")
        print(f"   Категория: {product['category']}")
        print(f"   Статус: {product['reason']}")
        
        if product['needs_form']:
            products_to_update.append(product)
            print("   🔧 Требует добавления формы")
        else:
            print("   ✅ Форма уже есть")
        print()
    
    if not products_to_update:
        print("🎉 Все продукты уже имеют формы!")
        return
    
    print(f"🔧 ОБНОВЛЕНИЕ {len(products_to_update)} ПРОДУКТОВ:")
    print()
    
    updated_count = 0
    
    for product in products_to_update:
        print(f"🔨 Обновляем {product['name']} ({product['id']})...")
        
        # Создаем форму для продукта
        new_interfaces = create_form_for_product(product)
        
        # Показываем, что будет добавлено
        input_fields = list(new_interfaces['input']['properties'].keys())
        required_fields = new_interfaces['input'].get('required', [])
        
        print(f"   Добавляем поля: {', '.join(input_fields)}")
        print(f"   Обязательные: {', '.join(required_fields)}")
        
        # Обновляем файл
        if update_product_file(product, new_interfaces):
            updated_count += 1
        
        print()
    
    print("=" * 60)
    print(f"🎯 РЕЗУЛЬТАТ: Обновлено {updated_count} из {len(products_to_update)} продуктов")
    
    if updated_count > 0:
        print("\n🔄 Рекомендуется перезапустить приложение для применения изменений")


if __name__ == "__main__":
    main()
