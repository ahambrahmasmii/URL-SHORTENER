# 📘 URL Shortener API Documentation

**Base URL:** `http://localhost:5000/`

---

## 📌 Overview

This service allows users to:

- 🔗 Shorten long URLs
- 🔁 Redirect using the short code
- 📊 Fetch analytics for a short URL

---

## 1. 🔗 Shorten URL

**Endpoint:** `POST /api/shorten`

**Description:**\
Accepts a long URL and returns a shortened URL. If the URL was previously shortened, returns the same short code.

### Request

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "url": "https://example.com/some/very/long/link"
}
```

### Success Response

**Status Code:** `201 Created`

**Body:**

```json
{
  "short_code": "a1B2c3",
  "short_url": "http://localhost:5000/a1B2c3"
}
```

### Error Response

**Status Code:** `400 Bad Request`

**Body:**

```json
{
  "error": "Invalid URL"
}
```

---

## 2. 🔁 Redirect to Long URL

**Endpoint:** `GET /<short_code>`

**Description:**\
Redirects to the original long URL associated with the given short code.

### Example

**Request:**\
`GET http://localhost:5000/a1B2c3`

### Success Response

**Status Code:** `302 Found`\
**Redirects To:** `https://example.com/some/very/long/link`

### Error Response

**Status Code:** `404 Not Found`

**Body:**

```json
{
  "error": "Short code not found"
}
```

---

## 3. 📊 Get URL Analytics

**Endpoint:** `GET /api/stats/<short_code>`

**Description:**\
Returns statistics for the given short code, including original URL, total clicks, and creation time.

### Example

**Request:**\
`GET http://localhost:5000/api/stats/a1B2c3`

### Success Response

**Status Code:** `200 OK`

**Body:**

```json
{
  "url": "https://example.com/some/very/long/link",
  "clicks": 5,
  "created_at": "2025-07-24T13:01:15.091510"
}
```

### Error Response

**Status Code:** `404 Not Found`

**Body:**

```json
{
  "error": "Short code not found"
}
```

---

## 🔒 Notes

- The same long URL always generates the same short code (deterministic hashing).
- URL mappings are stored in memory with optional JSON file persistence.
- The short code is 6 characters long, using alphanumeric Base62 encoding.
- Thread-safe and supports concurrent requests.

