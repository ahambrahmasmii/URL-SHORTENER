from flask import request, jsonify, redirect
from app.services import shorten_long_url, get_original_url, get_url_stats

def register_routes(app, storage):
    @app.route('/api/shorten', methods=['POST'])
    def shorten_url():
        data = request.get_json()
        long_url = data.get('url')
        return shorten_long_url(long_url, request.host_url, storage)

    @app.route('/<short_code>', methods=['GET'])
    def redirect_to_url(short_code):
        return get_original_url(short_code, storage)

    @app.route('/api/stats/<short_code>', methods=['GET'])
    def get_stats(short_code):
        return get_url_stats(short_code, storage)
