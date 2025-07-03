"""
Продукт: Мониторинг и анализ новостей
"""

from typing import Dict, List, Any
from ..products import BaseProduct
from ..llm_service import LLMService
import requests
import json
from datetime import datetime, timedelta

class NewsAnalysisProduct(BaseProduct):
    """Продукт для мониторинга и анализа отраслевых новостей"""
    
    def __init__(self, llm_service: LLMService):
        super().__init__(
            product_id="news_analysis",
            name="Мониторинг и анализ новостей",
            description="Автоматический мониторинг отраслевых новостей с ИИ-анализом и выявлением трендов"
        )
        self.llm_service = llm_service
        
        # Устанавливаем демо-данные
        self.set_demo_data({
            "monitored_sectors": [
                "Внешнеэкономическая деятельность",
                "Логистика и транспорт",
                "IT и цифровизация",
                "Финансы и банкинг",
                "Юридические изменения",
                "Государственные закупки"
            ],
            "news_sources": [
                "РБК", "Коммерсант", "Ведомости", "ТАСС",
                "Отраслевые издания", "Государственные порталы",
                "Профессиональные сообщества"
            ],
            "analysis_features": [
                "Sentiment анализ новостей",
                "Выявление трендов и паттернов",
                "Классификация по отраслям",
                "Оценка влияния на бизнес",
                "Автоматические уведомления"
            ],
            "update_frequency": "В режиме реального времени",
            "retention_period": "12 месяцев"
        })
    
    def get_product_info(self) -> Dict[str, Any]:
        """Информация о продукте для SEO-страниц"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "key_benefits": [
                "Отслеживание упоминаний компании/отрасли",
                "Раннее выявление рыночных трендов",
                "Анализ конкурентной среды",
                "Мониторинг регуляторных изменений",
                "Автоматические отчеты и уведомления"
            ],
            "target_audience": [
                "Экспортно-импортные компании",
                "Логистические операторы",
                "Консалтинговые фирмы",
                "Инвестиционные компании",
                "Государственные структуры",
                "Отраслевые аналитики"
            ],
            "use_cases": [
                "Мониторинг ВЭД изменений",
                "Отслеживание логистических трендов",
                "Анализ влияния санкций",
                "Мониторинг валютного законодательства",
                "Отслеживание цифровых инициатив",
                "Анализ государственных программ"
            ],
            "demo_available": True,
            "screenshots": self.get_screenshots(),
            "pricing": {
                "basic": "10 ключевых слов",
                "professional": "50 ключевых слов + аналитика",
                "enterprise": "Неограниченно + API"
            }
        }

    def get_input_interface_description(self) -> Dict[str, Any]:
        """
        Описывает ожидаемый формат входных данных для execute_demo.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Ключевое слово или фраза для поиска и анализа новостей.",
                    "example": "внешнеэкономическая деятельность"
                }
            },
            "required": ["query"]
        }

    def get_output_interface_description(self) -> Dict[str, Any]:
        """
        Описывает формат выходных данных из execute_demo.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Исходный запрос, по которому проводился анализ."
                },
                "total_news": {
                    "type": "integer",
                    "description": "Общее количество проанализированных новостей."
                },
                "news_items": {
                    "type": "array",
                    "description": "Список проанализированных новостных статей.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Заголовок новости."},
                            "content": {"type": "string", "description": "Содержание новости."},
                            "source": {"type": "string", "description": "Источник новости."},
                            "published_at": {"type": "string", "description": "Дата публикации новости в формате ISO 8601."},
                            "url": {"type": "string", "description": "URL новости."},
                            "analysis": {"type": "string", "description": "Результат ИИ-анализа новости (тональность, влияние, ключевые моменты)."}
                        }
                    }
                },
                "summary": {
                    "type": "string",
                    "description": "Сводный анализ по всем новостям, включая общие тренды и рекомендации.",
                    "example": "Общий тренд положительный..."
                },
                "trends": {
                    "type": "array",
                    "description": "Список выявленных трендов.",
                    "items": {"type": "string"}
                },
                "sentiment": {
                    "type": "object",
                    "description": "Общая тональность новостей (позитивная, нейтральная, негативная).",
                    "properties": {
                        "positive": {"type": "number", "format": "float", "description": "Доля позитивных новостей."},
                        "neutral": {"type": "number", "format": "float", "description": "Доля нейтральных новостей."},
                        "negative": {"type": "number", "format": "float", "description": "Доля негативных новостей."}
                    }
                }
            }
        }
    
    def execute_demo(self, input_data: Any) -> Dict[str, Any]:
        """Выполняет демо-анализ новостей"""
        query = input_data.get('query', 'внешнеэкономическая деятельность') if isinstance(input_data, dict) else str(input_data)
        
        try:
            # Генерируем демо-новости (в реальности здесь будет API новостных агрегаторов)
            demo_news = self._generate_demo_news(query)
            
            # Анализируем каждую новость через LLM
            analyzed_news = []
            for news_item in demo_news:
                analysis = self._analyze_news_item(news_item, query)
                analyzed_news.append({
                    **news_item,
                    "analysis": analysis
                })
            
            # Создаем сводный анализ
            summary_analysis = self._create_summary_analysis(analyzed_news, query)
            
            return {
                "query": query,
                "total_news": len(analyzed_news),
                "news_items": analyzed_news,
                "summary": summary_analysis,
                "trends": self._extract_trends(analyzed_news),
                "sentiment": self._calculate_overall_sentiment(analyzed_news)
            }
            
        except Exception as e:
            return {"error": f"Ошибка анализа новостей: {str(e)}"}
    
    def get_seo_keywords(self) -> List[str]:
        """Ключевые слова для SEO"""
        return [
            "мониторинг новостей",
            "анализ новостей ИИ",
            "отраслевой мониторинг",
            "мониторинг упоминаний",
            "анализ новостей ВЭД",
            "мониторинг внешнеэкономической деятельности",
            "логистические новости анализ",
            "мониторинг регуляторных изменений",
            "автоматический мониторинг СМИ",
            "анализ отраслевых трендов",
            "мониторинг конкурентов",
            "новостная аналитика",
            "медиа мониторинг",
            "sentiment анализ новостей",
            "мониторинг репутации бренда",
            "анализ рыночных трендов"
        ]
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Демо-контент для SEO-страниц"""
        return {
            "demo_queries": [
                "внешнеэкономическая деятельность",
                "логистика и транспорт",
                "цифровизация бизнеса",
                "валютное законодательство",
                "таможенное регулирование"
            ],
            
            "sample_analysis": {
                "positive_news": "65%",
                "neutral_news": "25%", 
                "negative_news": "10%",
                "trend_direction": "Положительный",
                "key_topics": [
                    "Упрощение экспортных процедур",
                    "Цифровизация таможни",
                    "Новые торговые соглашения"
                ]
            },
            
            "demo_screenshot_description": "Дашборд мониторинга показывает ленту новостей в реальном времени, аналитические графики по тональности и трендам, а также детальный анализ каждой новости с выделением ключевых моментов.",
            
            "monitoring_sectors": [
                "ВЭД и международная торговля",
                "Логистика и складирование", 
                "IT и цифровые технологии",
                "Финансовые услуги",
                "Промышленность и производство"
            ],
            
            "analysis_metrics": [
                "Тональность (позитив/негатив/нейтрал)",
                "Влияние на отрасль (высокое/среднее/низкое)",
                "Географический охват",
                "Ключевые участники рынка",
                "Потенциальные риски и возможности"
            ]
        }
    
    def _generate_demo_news(self, query: str) -> List[Dict[str, Any]]:
        """Генерирует демо-новости для показа"""
        # В реальности здесь будет интеграция с новостными API
        demo_templates = [
            {
                "title": f"Новые изменения в регулировании сферы '{query}'",
                "content": f"Министерство объявило о важных изменениях в регулировании {query}. Эксперты отмечают положительное влияние на развитие отрасли.",
                "source": "РБК",
                "published_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "url": "https://example.com/news/1"
            },
            {
                "title": f"Аналитики прогнозируют рост в сфере {query}",
                "content": f"Согласно исследованию ведущих аналитиков, сфера {query} покажет значительный рост в следующем квартале.",
                "source": "Ведомости",
                "published_at": (datetime.now() - timedelta(hours=5)).isoformat(),
                "url": "https://example.com/news/2"
            },
            {
                "title": f"Цифровизация в {query}: новые возможности",
                "content": f"Внедрение цифровых технологий в {query} открывает новые перспективы для бизнеса и повышения эффективности.",
                "source": "Коммерсант",
                "published_at": (datetime.now() - timedelta(hours=8)).isoformat(),
                "url": "https://example.com/news/3"
            }
        ]
        return demo_templates
    
    def _analyze_news_item(self, news_item: Dict[str, Any], query: str) -> str:
        """Анализирует отдельную новость через LLM"""
        prompt = f"""
        Проанализируй следующую новость в контексте темы "{query}":
        
        Заголовок: {news_item['title']}
        Содержание: {news_item['content']}
        
        Проведи анализ по следующим критериям:
        1. Тональность (позитивная/негативная/нейтральная)
        2. Влияние на отрасль (высокое/среднее/низкое) 
        3. Ключевые моменты
        4. Потенциальные последствия
        
        Ответ дай в формате краткого анализа до 200 слов.
        """
        
        try:
            analysis = self.llm_service.generate_text(prompt)
            return analysis
        except Exception as e:
            return f"Ошибка анализа: {str(e)}"
    
    def _create_summary_analysis(self, analyzed_news: List[Dict[str, Any]], query: str) -> str:
        """Создает сводный анализ по всем новостям"""
        news_summaries = [item.get('analysis', '') for item in analyzed_news]
        
        prompt = f"""
        На основе анализа новостей по теме "{query}" создай общий сводный анализ.
        
        Анализы отдельных новостей:
        {chr(10).join(news_summaries[:3])}  # Берем первые 3 для примера
        
        Создай сводку включающую:
        1. Общие тренды
        2. Ключевые изменения
        3. Рекомендации для бизнеса
        4. Прогноз развития
        
        Ответ в формате до 300 слов.
        """
        
        try:
            summary = self.llm_service.generate_text(prompt)
            return summary
        except Exception as e:
            return f"Ошибка создания сводки: {str(e)}"
    
    def _extract_trends(self, analyzed_news: List[Dict[str, Any]]) -> List[str]:
        """Извлекает тренды из новостей"""
        # Упрощенная версия - в реальности более сложная логика
        return [
            "Усиление цифровизации процессов",
            "Повышение регуляторных требований", 
            "Рост международного сотрудничества"
        ]
    
    def _calculate_overall_sentiment(self, analyzed_news: List[Dict[str, Any]]) -> Dict[str, float]:
        """Рассчитывает общую тональность"""
        # Упрощенная версия - в реальности анализ через LLM
        return {
            "positive": 0.6,
            "neutral": 0.3,
            "negative": 0.1
        }
