"""
Продукт: Анализ договоров с ИИ
"""

from typing import Dict, List, Any
from ..products import BaseProduct
from ..llm_service import LLMService
from ..parsing_service import ParsingService
from ..cache_service import CacheService
import markdown

class ContractAnalysisProduct(BaseProduct):
    """Продукт для анализа юридических договоров"""
    
    def __init__(self, llm_service: LLMService, parsing_service: ParsingService, cache_service: CacheService):
        super().__init__(
            product_id="contract_analysis",
            name="Анализ договоров с ИИ",
            description="Автоматизированный анализ юридических договоров с выявлением рисков и рекомендациями"
        )
        self.llm_service = llm_service
        self.parsing_service = parsing_service
        self.cache_service = cache_service
        
        # Устанавливаем демо-данные
        self.set_demo_data({
            "demo_contract_types": [
                "Договор аренды недвижимости",
                "Договор поставки товаров", 
                "Трудовой договор",
                "Договор оказания IT-услуг",
                "Договор подряда",
                "Кредитный договор"
            ],
            "key_features": [
                "Анализ рисков по каждому пункту",
                "Рекомендации по улучшению формулировок",
                "Проверка соответствия законодательству",
                "Выявление противоречий между разделами",
                "Оценка финансовых обязательств"
            ],
            "supported_formats": ["PDF", "DOC", "DOCX", "TXT"],
            "analysis_time": "2-5 минут",
            "accuracy": "95%"
        })
    
    def get_product_info(self) -> Dict[str, Any]:
        """Информация о продукте для SEO-страниц"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "key_benefits": [
                "Экономия времени юристов до 80%",
                "Снижение рисков пропуска важных моментов",
                "Стандартизация процесса анализа",
                "Круглосуточная доступность",
                "Детальные отчеты с рекомендациями"
            ],
            "target_audience": [
                "Юридические фирмы",
                "Корпоративные юристы", 
                "Малый и средний бизнес",
                "Индивидуальные предприниматели",
                "Государственные организации"
            ],
            "use_cases": [
                "Проверка договоров до подписания",
                "Аудит существующих договоров",
                "Обучение молодых юристов",
                "Массовая обработка типовых договоров",
                "Подготовка к судебным разбирательствам"
            ],
            "demo_available": True,
            "screenshots": self.get_screenshots(),
            "pricing": {
                "free_tier": "5 договоров в месяц",
                "pro_tier": "Неограниченно",
                "enterprise": "Корпоративные решения"
            }
        }

    def get_input_interface_description(self) -> Dict[str, Any]:
        """
        Описывает ожидаемый формат входных данных для execute_demo.
        """
        return {
            "type": "object",
            "properties": {
                "contract_text": {
                    "type": "string",
                    "description": "Полный текст юридического договора для анализа.",
                    "example": "Договор аренды нежилого помещения..."
                }
            },
            "required": ["contract_text"]
        }

    def get_output_interface_description(self) -> Dict[str, Any]:
        """
        Описывает формат выходных данных из execute_demo.
        """
        return {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Краткое резюме результатов анализа договора.",
                    "example": "Анализ договора завершен"
                },
                "paragraphs": {
                    "type": "array",
                    "description": "Список проанализированных абзацев договора.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "original_paragraph": {
                                "type": "string",
                                "description": "Исходный текст абзаца."
                            },
                            "analysis": {
                                "type": "string",
                                "description": "HTML-представление анализа данного абзаца, включая выявленные риски и рекомендации."
                            }
                        }
                    }
                },
                "stats": {
                    "type": "object",
                    "description": "Статистика по анализу.",
                    "properties": {
                        "total_paragraphs": {
                            "type": "integer",
                            "description": "Общее количество абзацев в договоре."
                        },
                        "analyzed_paragraphs": {
                            "type": "integer",
                            "description": "Количество проанализированных абзацев."
                        },
                        "cached_results": {
                            "type": "integer",
                            "description": "Количество результатов, взятых из кэша."
                        }
                    }
                }
            }
        }
    
    def execute_demo(self, input_data: Any) -> Dict[str, Any]:
        """Выполняет демо-анализ договора"""
        contract_text = input_data.get('contract_text', '') if isinstance(input_data, dict) else str(input_data)
        
        if not contract_text:
            return {"error": "Текст договора не предоставлен"}
        
        try:
            # Сегментация текста
            paragraphs = self.llm_service.segment_text_into_paragraphs(contract_text)
            
            # Анализ каждого абзаца
            analyzed_paragraphs = []
            file_hash = self.cache_service._generate_hash(contract_text)
            
            for i, paragraph in enumerate(paragraphs):
                analysis_html = self.cache_service.get_cached_paragraph_analysis(file_hash, paragraph)
                
                if not analysis_html:
                    # Анализ через LLM
                    analysis_markdown = self.llm_service.analyze_paragraph_in_context(paragraph, contract_text)
                    if analysis_markdown:
                        analysis_html = markdown.markdown(analysis_markdown)
                        self.cache_service.save_paragraph_analysis_to_cache(file_hash, paragraph, analysis_html)
                    else:
                        analysis_html = "Не удалось получить анализ для этого пункта."
                
                analyzed_paragraphs.append({
                    "original_paragraph": paragraph,
                    "analysis": analysis_html
                })
            
            return {
                "summary": "Анализ договора завершен",
                "paragraphs": analyzed_paragraphs,
                "stats": {
                    "total_paragraphs": len(paragraphs),
                    "analyzed_paragraphs": len(analyzed_paragraphs),
                    "cached_results": sum(1 for p in analyzed_paragraphs if "кэш" in p.get("analysis", ""))
                }
            }
            
        except Exception as e:
            return {"error": f"Ошибка анализа: {str(e)}"}
    
    def get_seo_keywords(self) -> List[str]:
        """Ключевые слова для SEO"""
        return [
            "анализ договора",
            "проверка договора", 
            "экспертиза договора",
            "анализ договора ИИ",
            "проверка контракта",
            "юридический анализ",
            "анализ рисков договора",
            "автоматический анализ договора",
            "проверка договора онлайн",
            "анализ условий договора",
            "договор аренды анализ",
            "договор поставки проверка",
            "трудовой договор анализ",
            "IT договор экспертиза",
            "кредитный договор проверка",
            "договор подряда анализ"
        ]
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Демо-контент для SEO-страниц"""
        return {
            "demo_contract_text": """Договор (данные придуманы)

ДОГОВОР АРЕНДЫ НЕЖИЛОГО ПОМЕЩЕНИЯ

г. Москва                                                        "15" января 2025 г.

ООО "Арендодатель Плюс", в лице директора Иванова Ивана Ивановича, действующего на основании Устава, именуемое в дальнейшем "Арендодатель", с одной стороны, и ИП Петров Петр Петрович, именуемый в дальнейшем "Арендатор", с другой стороны, заключили настоящий Договор о нижеследующем:

1. ПРЕДМЕТ ДОГОВОРА
1.1. Арендодатель предоставляет, а Арендатор принимает в аренду нежилое помещение общей площадью 50 кв.м., расположенное по адресу: г. Москва, ул. Примерная, д. 10, помещение 15.

2. СРОК ДОГОВОРА
2.1. Договор заключается на срок 11 месяцев с "01" февраля 2025 г. по "31" декабря 2025 г.

3. АРЕНДНАЯ ПЛАТА
3.1. Размер ежемесячной арендной платы составляет 80 000 (восемьдесят тысяч) рублей.
3.2. Арендная плата вносится до 10 числа текущего месяца.""",
            
            "expected_analysis_points": [
                "Проверка полноты реквизитов сторон",
                "Анализ размера арендной платы",
                "Оценка срока договора",
                "Проверка описания объекта аренды",
                "Анализ условий оплаты"
            ],
            
            "demo_screenshot_description": "Интерфейс анализа показывает текст договора с подсвеченными пунктами и панель с детальным анализом каждого раздела, включая выявленные риски и рекомендации.",
            
            "process_steps": [
                "Загрузка документа (PDF, DOC, TXT)",
                "Автоматическое извлечение текста",
                "Сегментация на смысловые блоки", 
                "ИИ-анализ каждого пункта",
                "Формирование отчета с рекомендациями"
            ]
        }
    
    def get_contract_types_mapping(self) -> Dict[str, str]:
        """Маппинг типов договоров к ключевым словам"""
        return {
            "аренды": "договор аренды",
            "поставки": "договор поставки",
            "подряда": "договор подряда", 
            "трудовой": "трудовой договор",
            "it-услуг": "договор IT-услуг",
            "кредитный": "кредитный договор",
            "страхования": "договор страхования",
            "лизинга": "договор лизинга",
            "франчайзинга": "договор франчайзинга",
            "инвестиций": "инвестиционный договор"
        }
