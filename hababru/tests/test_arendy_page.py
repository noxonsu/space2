import pytest
import os
import json
import markdown
import yaml
from bs4 import BeautifulSoup
from src.backend.main import create_app

@pytest.fixture
def real_client():
    """Фикстура для создания клиента Flask без мокирования LLMService."""
    test_app = create_app() # Создаем приложение без моков для LLMService
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client

def test_arendy_page_contract_and_analysis_display(real_client):
    """
    Тест проверяет, что при переходе на страницу /arendy:
    1. Возвращается статус 200 OK.
    2. В HTML-ответе присутствует заголовок страницы из source.md.
    3. В HTML-ответе присутствует основной текст страницы из source.md.
    4. В скрытом div с id="app-config-data" корректно переданы:
       - seoPageContractTextRaw (текст договора из generated_contract.txt)
       - analysisResultsRaw (результаты анализа, не пустые)
    """
    seo_page_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'seo_pages', 'arendy')
    source_md_path = os.path.join(seo_page_dir, 'source.md')
    generated_contract_path = os.path.join(seo_page_dir, 'generated_contract.txt')

    # 1. Читаем ожидаемый контент из source.md
    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    parts = source_content.split('---', 2)
    front_matter = yaml.safe_load(parts[1])
    page_text_content_md = parts[2].strip()
    expected_page_text_html = markdown.markdown(page_text_content_md)

    # 2. Читаем ожидаемый текст договора из generated_contract.txt
    with open(generated_contract_path, 'r', encoding='utf-8') as f:
        expected_contract_text = f.read()

    # 3. Выполняем GET-запрос к /arendy
    rv = real_client.get('/arendy')
    assert rv.status_code == 200, f"Ожидался статус 200, получен {rv.status_code}"

    # 4. Проверяем наличие заголовка и основного текста страницы
    assert front_matter['title'].encode('utf-8') in rv.data, "Заголовок страницы не найден в ответе"
    assert expected_page_text_html.encode('utf-8') in rv.data, "Основной текст страницы не найден в ответе"

    # 5. Извлекаем и проверяем данные из app-config-data
    soup = BeautifulSoup(rv.data, 'html.parser')
    app_config_div = soup.find('div', id='app-config-data')
    assert app_config_div is not None, "Не удалось найти div с id='app-config-data'"
    
    app_config_json_string = app_config_div.text.strip()
    assert app_config_json_string, "div с id='app-config-data' пуст"
    
    app_config = json.loads(app_config_json_string)

    assert app_config.get('isSeoPage') is True, "isSeoPage не True"
    assert app_config.get('mainKeyword') == front_matter['main_keyword'], "mainKeyword не соответствует"
    assert app_config.get('seoPageContractTextRaw') == expected_contract_text, "seoPageContractTextRaw не соответствует ожидаемому тексту договора"
    
    # Проверяем, что analysis_results_raw присутствует и содержит непустой массив paragraphs
    assert 'analysis_results_raw' in app_config, "analysis_results_raw отсутствует в appConfig"
    analysis_results = app_config['analysis_results_raw']
    assert isinstance(analysis_results, dict), "analysis_results_raw должен быть словарем"
    assert 'paragraphs' in analysis_results, "analysis_results_raw не содержит ключ 'paragraphs'"
    assert isinstance(analysis_results['paragraphs'], list), "paragraphs должен быть списком"
    assert len(analysis_results['paragraphs']) > 0, "Список paragraphs пуст, анализ не был выполнен"
    
    # Дополнительная проверка структуры первого элемента анализа
    first_paragraph_analysis = analysis_results['paragraphs'][0]
    assert 'original_paragraph' in first_paragraph_analysis, "Первый пункт анализа не содержит 'original_paragraph'"
    assert 'analysis' in first_paragraph_analysis, "Первый пункт анализа не содержит 'analysis'"
