import pytest
from src.backend.main import create_app # Изменено на create_app

@pytest.fixture
def client():
    test_app = create_app() # Используем create_app()
    test_app.config['TESTING'] = True
    with test_app.test_client() as client: # Используем test_app
        yield client

def test_seo_admin_page_loads(client):
    """
    Tests if the /seo_admin page loads successfully.
    """
    response = client.get('/seo_admin')
    assert response.status_code == 302  # Expect a redirect
    assert 'Location' in response.headers
    assert response.headers['Location'] == '/admin'

    # Follow the redirect
    redirect_response = client.get(response.headers['Location'])
    assert redirect_response.status_code == 200
    assert 'Дашборд' in redirect_response.data.decode('utf-8')
