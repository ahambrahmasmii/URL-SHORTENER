import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:5000"
LONG_URL = "https://example.com"


response = requests.post(f"{BASE_URL}/api/shorten", json={"url": LONG_URL})
short_code = response.json()["short_code"]
short_url = f"{BASE_URL}/{short_code}"

print(f"Shortened URL: {short_url}")


def simulate_click():
    return requests.get(short_url)


concurrent_users = 1000
with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
    futures = [executor.submit(simulate_click) for _ in range(concurrent_users)]


print("All clicks sent.")


stats = requests.get(f"{BASE_URL}/api/stats/{short_code}")
print("Final stats:", stats.json())
