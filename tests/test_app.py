import pytest 
import os 
import sys 
from flask import Flask, request, render_template_string 

# Adjust sys.path to include the parent directory (project-root) of tests/ 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from app import app 

@pytest.fixture 
def client(): 
    app.config['TESTING'] = True 
    with app.test_client() as client: 
        yield client 

def test_index_page(client): 
    response = client.get('/') 
    assert response.status_code == 200 
    assert b"Language Translation App" in response.data 

def test_translate_endpoint_missing_data(client): 
    response = client.post('/translate') 
    assert response.status_code == 400 
    assert b'Missing form data' in response.data 

def test_translate_endpoint_valid_data(client): 
    data = { 
        'source_text': 'Hello, how are you?', 
        'source_lang': 'en', 
        'target_lang': 'fr', 
        'formality': 'neutral', 
        'domain': 'general' 
    } 
    response = client.post('/translate', data=data) 
    assert response.status_code == 200 
    assert b'Translated Text' in response.data 

def test_invalid_route(client): 
    response = client.get('/invalid-route') 
    assert response.status_code == 404 
    assert b'<h1>404 - Page Not Found</h1>' in response.data 
 
def test_internal_server_error(client, monkeypatch): 
    data = { 
        'source_text': 'Hello, how are you?', 
        'source_lang': 'en', 
        'target_lang': 'fr', 
        'formality': 'neutral', 
        'domain': 'general' 
    } 

    def mock_translate_text(*args, **kwargs): 
        raise Exception('Test error') 

    monkeypatch.setattr('app.translate_text', mock_translate_text) 

    response = client.post('/translate', data=data) 
    assert response.status_code == 500 
    assert b'Unexpected error' in response.data 