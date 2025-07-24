# URL Shortener – Design Notes & Implementation Approach

## 1. Overview

This project is a simplified URL shortener service (like bit.ly or tinyurl), implemented in Python using Flask. It allows users to shorten long URLs, retrieve analytics, and handle redirection — all with in-memory storage and persistent disk support.

---

## 2. Design Goals

- ✅ Keep the implementation **clean, readable, and testable**
- ✅ Ensure **thread-safe concurrent access**
- ✅ Avoid external dependencies (no database or Redis)
- ✅ Include **deterministic** short code generation for idempotency
- ✅ Provide **persistent storage** to avoid data loss across restarts

---

## 3. Core Components

### 3.1 `URLStore` (in `storage.py`)
- Maintains an in-memory `url_map` dict:  
  `{ short_code → {url, clicks, created_at} }`
- Uses a **`threading.Lock()`** to guard all reads/writes (ensuring thread safety)
- Loads from `data.json` at startup and writes to it after every update

### 3.2 Routes (in `routes.py`)
- `POST /api/shorten`: Shortens a URL deterministically
- `GET /<short_code>`: Redirects to the original long URL and tracks click count
- `GET /api/stats/<short_code>`: Returns analytics (clicks, created_at, long URL)

### 3.3 Short Code Generation (`utils.py`)
- Uses **SHA-256 hash** of the input URL → converts to **Base62** → fixed-length code
- Ensures same URL always generates the same short code (no random duplication)
- 6-character alphanumeric code, ~56.8 billion unique possibilities

---

## 4. Implementation Choices & Rationale

### 4.1 ✅ Deterministic Short Codes (Hash-based)
- Prevents storing multiple entries for the same URL
- Avoids needing a `reverse_map`
- Simpler and more space-efficient than random generators

### 4.2 ✅ File-based Persistence (`data.json`)
- Provides crash recovery and restart safety
- No need for external databases — suitable for assignments, MVPs, and small tools
- Saves on every write for maximum safety (no batching)

### 4.3 ✅ Thread Safety with `threading.Lock`
- Flask dev server and WSGI servers like Gunicorn may serve requests in parallel
- Lock ensures `url_map` is never read or modified concurrently without coordination

### 4.4 ✅ In-Memory Design
- Fast lookups (`O(1)`)
- Behaves like a cache by default
- Suitable until horizontal scaling is needed

---

## 5. Assumptions

- Short codes are unique and based on hashing the long URL
- No URL expiration logic or deletion is implemented
- The server runs on a single instance (not yet horizontally scalable)
- Not using rate limiting or auth for simplicity

---

## 6. Potential Future Enhancements

| Feature                  | Description                                |
|--------------------------|--------------------------------------------|
| SQLite or Redis support  | Replace in-memory with a database        |
| Expiry / TTL             | Allow time-based cleanup of old entries    |
| Custom short codes       | Let users choose their own codes           |
| Rate limiting            | Prevent abuse via IP-level request limits  |
| Dockerization            | Containerize for portability               |
| RESTful validation       | Use marshmallow or Pydantic for schemas    |
| Analytics dashboard      | Add UI to view stats                       |

---

## 7. Running the App

```bash
# Start the Flask app
python -m flask --app app.main run

# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Redirect
curl -L http://localhost:5000/<short_code>

# Stats
curl http://localhost:5000/api/stats/<short_code>
```

---

## 8. Summary

This solution is optimized for:
- Simplicity
- Reliability
- Determinism
- Safety under concurrency

It offers a robust starting point that can be evolved into a production-grade system with minimal refactoring.

---
