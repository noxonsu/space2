import os
import pytest
from unittest.mock import MagicMock, patch
from src.backend.services.seo_service import SeoService
from src.backend.services.llm_service import LLMService
from src.backend.services.parsing_service import ParsingService

@pytest.fixture
def seo_service():
    base_test_dir = "test_content_for_seo"
    content_dir = os.path.join(base_test_dir, "content", "seo_pages")
    os.makedirs(os.path.join(content_dir, "test-page"), exist_ok=True)
    with open(os.path.join(content_dir, "test-page", "source.md"), "w") as f:
        f.write("---\ntitle: Test Page\n---\n# Hello")
    with open(os.path.join(content_dir, "test-page", "generated_contract.txt"), "w") as f:
        f.write("Test contract")
    
    mock_llm_service = MagicMock(spec=LLMService)
    mock_parsing_service = MagicMock(spec=ParsingService)
    
    service = SeoService(llm_service=mock_llm_service, parsing_service=mock_parsing_service, content_base_path=content_dir)
    yield service
    
    # Teardown
    import shutil
    shutil.rmtree(base_test_dir)


def test_render_seo_page(seo_service):
    with patch('src.backend.services.seo_service.render_template') as mock_render:
        seo_service.render_seo_page("test-page")
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        assert kwargs['page_title'] == 'Test Page'

def test_render_nonexistent_seo_page(seo_service):
    with pytest.raises(FileNotFoundError):
        seo_service.render_seo_page("nonexistent-page")
