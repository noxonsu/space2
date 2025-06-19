import os
import json
import pytest
from src.backend.services.cache_service import CacheService

@pytest.fixture
def cache_service():
    cache_dir = "test_cache"
    service = CacheService(cache_dir=cache_dir)
    yield service
    # Teardown: remove the cache directory and its contents
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)

def test_create_analysis_task(cache_service):
    file_hash = "test_hash"
    total_items = 5
    task_id = cache_service.create_analysis_task(file_hash, total_items)
    
    task_status = cache_service.get_analysis_task_status(task_id)
    assert task_status is not None
    assert task_status["status"] == "PENDING"
    assert task_status["file_hash"] == file_hash
    assert task_status["total_items"] == total_items

def test_paragraph_caching(cache_service):
    file_hash = "test_file_hash"
    paragraph_text = "This is a test paragraph."
    analysis_html = "<p>This is the analysis.</p>"
    
    cache_service.save_paragraph_analysis_to_cache(file_hash, paragraph_text, analysis_html)
    
    cached_analysis = cache_service.get_cached_paragraph_analysis(file_hash, paragraph_text)
    assert cached_analysis == analysis_html
