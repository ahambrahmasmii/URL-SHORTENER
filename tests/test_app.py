import pytest
from app.main import app as flask_app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

# ------------------
# Tests for Shorten URL Endpoint
# ------------------

def test_shorten_url_success(client):
    """Shortening a valid URL returns 200 and contains short_code and short_url"""
    response = client.post('/api/shorten', json={'url': 'https://example.com/test'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert len(data['short_code']) == 6
    assert data['short_url'].endswith(data['short_code'])

def test_shorten_url_idempotent(client):
    """Shortening the same URL twice returns the same short_code"""
    url = 'https://example.com/unique'
    resp1 = client.post('/api/shorten', json={'url': url})
    code1 = resp1.get_json()['short_code']
    resp2 = client.post('/api/shorten', json={'url': url})
    code2 = resp2.get_json()['short_code']
    assert code1 == code2

def test_shorten_url_invalid_format(client):
    """Shortening an invalid URL returns a 400 error"""
    response = client.post('/api/shorten', json={'url': 'invalid-url'})
    assert response.status_code == 400

def test_shorten_url_missing_field(client):
    """Missing URL field in request returns 400 error"""
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400

def test_shorten_url_empty_string(client):
    """Sending an empty URL returns 400 error"""
    response = client.post('/api/shorten', json={'url': ''})
    assert response.status_code == 400

# ------------------
# Tests for Redirect Endpoint
# ------------------

def test_redirect_success_and_click_increment(client):
    """Accessing the short URL redirects and increments click count"""
    url = 'https://example.com/redirect'
    short_resp = client.post('/api/shorten', json={'url': url})
    code = short_resp.get_json()['short_code']

    # Redirect call
    redirect_resp = client.get(f'/{code}')
    assert redirect_resp.status_code == 302
    assert redirect_resp.location == url

    # Verify click count incremented
    stats = client.get(f'/api/stats/{code}').get_json()
    assert stats['clicks'] == 1


def test_redirect_not_found(client):
    """Redirecting with a non-existent short_code returns 404"""
    response = client.get('/non123')
    assert response.status_code == 404


def test_redirect_invalid_code_format(client):
    """Redirecting with malformed code returns 404 (or appropriate error)"""
    response = client.get('/!@#$%^')
    assert response.status_code == 404

# ------------------
# Tests for Analytics Endpoint
# ------------------

def test_stats_success(client):
    """Stats API returns correct data for existing short_code"""
    url = 'https://example.com/analytics'
    short_resp = client.post('/api/shorten', json={'url': url})
    code = short_resp.get_json()['short_code']

    # Call stats
    stats_resp = client.get(f'/api/stats/{code}')
    data = stats_resp.get_json()
    assert stats_resp.status_code == 200
    assert data['url'] == url
    assert isinstance(data['clicks'], int)
    assert 'created_at' in data


def test_stats_not_found(client):
    """Requesting stats for non-existent short_code returns 404"""
    response = client.get('/api/stats/ghost1')
    assert response.status_code == 404


def test_stats_invalid_code_format(client):
    """Malformed short_code in stats request returns 404 (or error)"""
    response = client.get('/api/stats/!@123*')
    assert response.status_code == 404
