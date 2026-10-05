import pytest
from src.preprocessing.text_cleaner import clean_text

def test_clean_text_basic():
    raw_text = "This is a Test! 123"
    assert clean_text(raw_text) == "this is a test 123"

def test_clean_text_html():
    raw_text = "<p>Hello <b>World</b></p>"
    assert clean_text(raw_text) == "hello world"

def test_clean_text_urls():
    raw_text = "Check this out https://example.com/page?id=1"
    assert clean_text(raw_text) == "check this out"

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""
