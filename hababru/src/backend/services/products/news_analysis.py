"""
Продукт: Мониторинг и анализ новостей
"""

from typing import Dict, List, Any
from ..products import BaseProduct
from ..llm_service import LLMService
from ..product_data_loader import ProductDataLoader
import requests
import json
from datetime import datetime, timedelta

class NewsAnalysisProduct(BaseProduct):
    """Продукт для мониторинга и анализа отраслевых новостей"""
    
    def __init__(self, llm_service: LLMService):
        # Загружаем данные из YAML-файла
        self.data_loader = ProductDataLoader()
        self.product_data = self.data_loader.load_product_data("news_analysis")
        
        super().__init__(
            product_id=self.product_data["product_id"],
            name=self.product_data["name"],
            description=self.product_data["description"]
        )
        self.llm_service = llm_service
        
        # Устанавливаем демо-данные из файла
        self.set_demo_data(self.product_data.get("demo_data", {}))
    
    def get_product_info(self) -> Dict[str, Any]:
        """Информация о продукте для SEO-страниц"""
        product_info = self.product_data.get("product_info", {})
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "key_benefits": product_info.get("key_benefits", []),
            "target_audience": product_info.get("target_audience", []),
            "use_cases": product_info.get("use_cases", []),
            "demo_available": product_info.get("demo_available", True),
            "screenshots": self.get_screenshots(),
            "pricing": product_info.get("pricing", {})
        }

    def get_input_interface_description(self) -> Dict[str, Any]:
        """
        Описывает ожидаемый формат входных данных для execute_demo.
        """
        return self.product_data.get("interfaces", {}).get("input", {})

    def get_output_interface_description(self) -> Dict[str, Any]:
        """
        Описывает формат выходных данных из execute_demo.
        """
        return self.product_data.get("interfaces", {}).get("output", {})
    
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
        return self.product_data.get("seo", {}).get("keywords", [])
    
    def get_demo_content(self) -> Dict[str, Any]:
        """Демо-контент для SEO-страниц"""
        return self.product_data.get("seo", {}).get("demo_content", {})
    
    def _generate_demo_news(self, query: str) -> List[Dict[str, Any]]:
        """Генерирует демо-новости для показа"""
        # Загружаем шаблоны из файла конфигурации
        demo_templates = self.product_data.get("demo_examples", {}).get("demo_news_templates", [])
        
        # Если шаблонов нет в файле, используем базовый пример
        if not demo_templates:
            demo_templates = [{
                "title": f"Новые изменения в регулировании сферы '{query}'",
                "content": f"Важные изменения в регулировании {query}",
                "source": "Новостной источник",
                "url_template": "https://example.com/news/{id}"
            }]
        
        result_news = []
        for i, template in enumerate(demo_templates):
            news_item = {
                "title": template["title"].format(query=query),
                "content": template["content"].format(query=query),
                "source": template["source"],
                "published_at": (datetime.now() - timedelta(hours=2*(i+1))).isoformat(),
                "url": template.get("url_template", "https://example.com/news/{id}").format(id=i+1)
            }
            result_news.append(news_item)
        
        return result_news
    
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
        # Берем тренды из конфигурации
        return self.product_data.get("demo_examples", {}).get("default_trends", [
            "Усиление цифровизации процессов",
            "Повышение регуляторных требований", 
            "Рост международного сотрудничества"
        ])
    
    def _calculate_overall_sentiment(self, analyzed_news: List[Dict[str, Any]]) -> Dict[str, float]:
        """Рассчитывает общую тональность"""
        # Берем дефолтные значения из конфигурации
        return self.product_data.get("demo_examples", {}).get("default_sentiment", {
            "positive": 0.6,
            "neutral": 0.3,
            "negative": 0.1
        })
