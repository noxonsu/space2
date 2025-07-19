#!/usr/bin/env python3
"""
Скрипт для анализа форм всех продуктов в системе
"""

import sys
import os
import yaml
import json
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hababru'))

from hababru.src.backend.services.product_data_loader import ProductDataLoader


def analyze_product_forms():
    print("=== АНАЛИЗ ФОРМ ВСЕХ ПРОДУКТОВ ===\n")
    
    # Инициализируем загрузчик данных
    data_loader = ProductDataLoader()
    
    # Получаем список всех продуктов
    try:
        available_products = data_loader.get_available_products()
        print(f"Найдено {len(available_products)} продуктов:")
        for product in available_products:
            print(f"  - {product}")
        print()
    except Exception as e:
        print(f"❌ Ошибка получения списка продуктов: {e}")
        return
    
    # Анализируем каждый продукт
    form_analysis = {}
    
    for product_id in available_products:
        try:
            print(f"📦 АНАЛИЗ ПРОДУКТА: {product_id}")
            print("─" * 60)
            
            # Загружаем данные продукта
            product_data = data_loader.load_product_data(product_id)
            
            # Анализируем интерфейсы
            interfaces = product_data.get('interfaces', {})
            input_interface = interfaces.get('input', {})
            output_interface = interfaces.get('output', {})
            
            # Информация о форме
            form_info = {
                'name': product_data.get('name', 'Не указано'),
                'category': product_data.get('category', 'Не указано'),
                'has_input_interface': bool(input_interface),
                'has_output_interface': bool(output_interface),
                'input_fields': [],
                'required_fields': [],
                'form_complexity': 'простая'
            }
            
            # Анализируем поля ввода
            if input_interface:
                properties = input_interface.get('properties', {})
                required = input_interface.get('required', [])
                
                print(f"✅ Есть интерфейс ввода:")
                print(f"   - Тип: {input_interface.get('type', 'не указан')}")
                print(f"   - Количество полей: {len(properties)}")
                print(f"   - Обязательных полей: {len(required)}")
                
                if properties:
                    print(f"   - Поля:")
                    for field_name, field_config in properties.items():
                        field_type = field_config.get('type', 'unknown')
                        field_desc = field_config.get('description', 'Без описания')
                        is_required = field_name in required
                        required_mark = " (обязательное)" if is_required else ""
                        print(f"     • {field_name}: {field_type} - {field_desc}{required_mark}")
                        
                        form_info['input_fields'].append({
                            'name': field_name,
                            'type': field_type,
                            'description': field_desc,
                            'required': is_required,
                            'example': field_config.get('example', 'Нет примера')
                        })
                        
                        if is_required:
                            form_info['required_fields'].append(field_name)
                
                # Определяем сложность формы
                if len(properties) > 5:
                    form_info['form_complexity'] = 'сложная'
                elif len(properties) > 2:
                    form_info['form_complexity'] = 'средняя'
            else:
                print("❌ Нет интерфейса ввода")
            
            # Анализируем интерфейс вывода
            if output_interface:
                output_properties = output_interface.get('properties', {})
                print(f"✅ Есть интерфейс вывода:")
                print(f"   - Тип: {output_interface.get('type', 'не указан')}")
                print(f"   - Количество полей в ответе: {len(output_properties)}")
                
                if output_properties:
                    print(f"   - Основные поля ответа:")
                    for field_name, field_config in list(output_properties.items())[:5]:  # Показываем первые 5
                        field_type = field_config.get('type', 'unknown')
                        field_desc = field_config.get('description', 'Без описания')[:50]
                        print(f"     • {field_name}: {field_type} - {field_desc}...")
                    if len(output_properties) > 5:
                        print(f"     ... и еще {len(output_properties) - 5} полей")
            else:
                print("❌ Нет интерфейса вывода")
            
            # Демо данные
            demo_data = product_data.get('demo_data', {})
            if demo_data:
                print(f"🎯 Демо-данные доступны: {len(demo_data)} секций")
            
            # Сохраняем анализ
            form_analysis[product_id] = form_info
            
            print("─" * 60)
            print()
            
        except Exception as e:
            print(f"❌ Ошибка анализа продукта {product_id}: {e}")
            print()
    
    # Сводный анализ
    print("=" * 80)
    print("📊 СВОДНЫЙ АНАЛИЗ ФОРМ")
    print("=" * 80)
    
    total_products = len(form_analysis)
    products_with_forms = sum(1 for info in form_analysis.values() if info['has_input_interface'])
    products_without_forms = total_products - products_with_forms
    
    print(f"Всего продуктов: {total_products}")
    print(f"С формами ввода: {products_with_forms}")
    print(f"Без форм ввода: {products_without_forms}")
    print()
    
    # Группировка по категориям
    categories = {}
    for product_id, info in form_analysis.items():
        category = info['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((product_id, info))
    
    print("🏷️ ГРУППИРОВКА ПО КАТЕГОРИЯМ:")
    for category, products in categories.items():
        print(f"\n📂 {category.upper()}:")
        for product_id, info in products:
            form_status = "✅ Есть форма" if info['has_input_interface'] else "❌ Нет формы"
            complexity = info['form_complexity']
            field_count = len(info['input_fields'])
            print(f"   • {info['name']} ({product_id}): {form_status}")
            if info['has_input_interface']:
                print(f"     ├─ Сложность: {complexity}")
                print(f"     ├─ Полей: {field_count}")
                print(f"     └─ Обязательных: {len(info['required_fields'])}")
    
    # Анализ уникальности форм
    print("\n🔍 АНАЛИЗ УНИКАЛЬНОСТИ ФОРМ:")
    
    form_signatures = {}
    for product_id, info in form_analysis.items():
        if info['has_input_interface']:
            # Создаем "подпись" формы на основе полей
            field_types = sorted([f['type'] for f in info['input_fields']])
            signature = tuple(field_types)
            
            if signature not in form_signatures:
                form_signatures[signature] = []
            form_signatures[signature].append((product_id, info['name']))
    
    unique_forms = 0
    similar_forms = 0
    
    for signature, products in form_signatures.items():
        if len(products) == 1:
            unique_forms += 1
            product_id, name = products[0]
            print(f"✨ Уникальная форма: {name} ({product_id}) - поля: {list(signature)}")
        else:
            similar_forms += len(products)
            print(f"🔄 Похожие формы ({len(products)} продуктов) - поля: {list(signature)}")
            for product_id, name in products:
                print(f"     • {name} ({product_id})")
    
    print(f"\nИтого:")
    print(f"  - Уникальных форм: {unique_forms}")
    print(f"  - Продуктов с похожими формами: {similar_forms}")
    print(f"  - Типов форм: {len(form_signatures)}")
    
    return form_analysis


if __name__ == "__main__":
    analysis = analyze_product_forms()
