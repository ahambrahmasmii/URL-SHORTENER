from flask import jsonify, redirect
from app.utils import is_valid_url, generate_deterministic_code

def shorten_long_url(long_url, host_url, storage):
    if not long_url or not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_deterministic_code(long_url)
    storage.add_if_absent(short_code, long_url)

    return jsonify({
        'short_code': short_code,
        'short_url': f"{host_url}{short_code}"
    }), 201


def get_original_url(short_code, storage):
    url = storage.get_url(short_code)
    if not url:
        return jsonify({'error': 'Short code not found'}), 404

    storage.increment_clicks(short_code)
    return redirect(url)


def get_url_stats(short_code, storage):
    analytics = storage.get_analytics(short_code)
    if not analytics:
        return jsonify({'error': 'Short code not found'}), 404

    return jsonify({
        'url': analytics['url'],
        'clicks': analytics['clicks'],
        'created_at': analytics['created_at'].isoformat()
    }), 200
