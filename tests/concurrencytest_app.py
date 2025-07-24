import requests
from concurrent.futures import ThreadPoolExecutor

# Change this if needed
BASE_URL = "http://127.0.0.1:5000"
LONG_URL = "https://example.com"

# Step 1: Create short URL
response = requests.post(f"{BASE_URL}/api/shorten", json={"url": LONG_URL})
short_code = response.json()["short_code"]
short_url = f"{BASE_URL}/{short_code}"

print(f"Shortened URL: {short_url}")

# Step 2: Simulate concurrent clicks
def simulate_click():
    return requests.get(short_url)

# Run 100 concurrent clicks
concurrent_users = 1000
with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
    futures = [executor.submit(simulate_click) for _ in range(concurrent_users)]

# Wait and check results
print("All clicks sent.")

# Step 3: Check click count
stats = requests.get(f"{BASE_URL}/api/stats/{short_code}")
print("Final stats:", stats.json())
