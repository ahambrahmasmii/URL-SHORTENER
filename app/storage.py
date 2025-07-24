from datetime import datetime
from threading import Lock

class URLStorage:
    def __init__(self):
        self.lock = Lock()
        self.url_map = {}

    def add_if_absent(self, short_code, long_url):
        with self.lock:
            if short_code not in self.url_map:
                self.url_map[short_code] = {
                    "url": long_url,
                    "clicks": 0,
                    "created_at": datetime.utcnow()
                }

    def get_url(self, short_code):
        with self.lock:
            entry = self.url_map.get(short_code)
            return entry["url"] if entry else None

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]["clicks"] += 1

    def get_analytics(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)
