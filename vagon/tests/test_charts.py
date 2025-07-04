import pytest
import pandas as pd
import sys
import os

# Добавляем путь к модулю
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import ChartGenerator

class TestChartGenerator:
    def setup_method(self):
        """Инициализация перед каждым тестом"""
        self.chart_generator = ChartGenerator()
    
    def test_chart_generator_init(self):
        """Тест инициализации генератора графиков"""
        assert self.chart_generator is not None
    
    def test_detect_chart_type_pie(self):
        """Тест определения типа графика - круговая диаграмма"""
        data = pd.DataFrame({
            'Категория': ['A', 'B', 'C'],
            'Значение': [10, 20, 30]
        })
        
        chart_type = self.chart_generator.detect_chart_type(data, "показать в разрезе родов груза")
        assert chart_type == 'pie'
        
        chart_type = self.chart_generator.detect_chart_type(data, "распределение по грузоотправителям")
        assert chart_type == 'pie'
    
    def test_detect_chart_type_bar(self):
        """Тест определения типа графика - столбчатая диаграмма"""
        data = pd.DataFrame({
            'Категория': ['A', 'B', 'C'],
            'Значение': [10, 20, 30]
        })
        
        chart_type = self.chart_generator.detect_chart_type(data, "топ 5 грузоотправителей")
        assert chart_type == 'bar'
        
        chart_type = self.chart_generator.detect_chart_type(data, "сравни объемы")
        assert chart_type == 'bar'
    
    def test_detect_chart_type_line(self):
        """Тест определения типа графика - линейный график"""
        data = pd.DataFrame({
            'Дата': ['2023-01', '2023-02', '2023-03'],
            'Значение': [100, 150, 200]
        })
        
        chart_type = self.chart_generator.detect_chart_type(data, "как менялась динамика")
        assert chart_type == 'line'
        
        chart_type = self.chart_generator.detect_chart_type(data, "показать тренд по месяцам")
        assert chart_type == 'line'
    
    def test_generate_chart_title(self):
        """Тест генерации заголовков графиков"""
        data = pd.DataFrame()
        
        title = self.chart_generator.generate_chart_title(data, "выгрузка вагонов")
        assert "выгрузка" in title.lower()
        
        title = self.chart_generator.generate_chart_title(data, "погрузка на суда")
        assert "погрузка" in title.lower()
        
        title = self.chart_generator.generate_chart_title(data, "по роду груза")
        assert "род груза" in title.lower()
    
    def test_create_chart_with_empty_data(self):
        """Тест создания графика с пустыми данными"""
        empty_data = pd.DataFrame()
        
        result = self.chart_generator.create_chart(empty_data, 'line', 'Тест', 'X', 'Y')
        assert result is None
    
    def test_create_chart_with_valid_data(self):
        """Тест создания графика с валидными данными"""
        data = pd.DataFrame({
            'Месяц': ['2023-01', '2023-02', '2023-03'],
            'Количество': [100, 150, 200]
        })
        
        result = self.chart_generator.create_chart(data, 'line', 'Тест', 'Месяц', 'Количество')
        assert result is not None
        assert isinstance(result, str)  # base64 строка
        assert len(result) > 0

if __name__ == '__main__':
    pytest.main([__file__])
