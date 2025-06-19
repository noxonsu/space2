import os
import pytest
from unittest.mock import MagicMock
from src.backend.services.parsing_service import ParsingService

@pytest.fixture
def parsing_service():
    mock_llm_service = MagicMock()
    return ParsingService(llm_service=mock_llm_service)

import io
from unittest.mock import patch, MagicMock

def test_parse_document_to_markdown_pdf(parsing_service):
    mock_markdown_converter = MagicMock()
    mock_markdown_converter.convert_stream.return_value.markdown = "Hello World."
    with patch('src.backend.services.parsing_service.MarkItDown', return_value=mock_markdown_converter):
        file_content = b"%PDF-1.4\n...\n" # Dummy PDF content
        file_stream = io.BytesIO(file_content)
        text = parsing_service.parse_document_to_markdown(file_stream, "test.pdf")
        assert "Hello World." in text
        mock_markdown_converter.convert_stream.assert_called_once_with(file_stream, filename="test.pdf")

def test_parse_document_to_markdown_docx(parsing_service):
    mock_markdown_converter = MagicMock()
    mock_markdown_converter.convert_stream.return_value.markdown = "Hello World."
    with patch('src.backend.services.parsing_service.MarkItDown', return_value=mock_markdown_converter):
        file_content = b"PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00...\n" # Dummy DOCX content
        file_stream = io.BytesIO(file_content)
        text = parsing_service.parse_document_to_markdown(file_stream, "test.docx")
        assert "Hello World." in text
        mock_markdown_converter.convert_stream.assert_called_once_with(file_stream, filename="test.docx")

def test_segment_text_into_paragraphs(parsing_service):
    parsing_service.llm_service.segment_text_into_paragraphs.return_value = ["First paragraph.", "Second paragraph.", "Third paragraph."]
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    segments = parsing_service.segment_text_into_paragraphs(text)
    assert len(segments) == 3
    assert segments[0] == "First paragraph."
    assert segments[1] == "Second paragraph."
    assert segments[2] == "Third paragraph."
    parsing_service.llm_service.segment_text_into_paragraphs.assert_called_once_with(text)
