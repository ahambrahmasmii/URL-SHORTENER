# URL Shortener 🔗

A simple in-memory URL shortener built using Python and Flask, with persistent storage via a JSON file.

---

## ✨ Features

- Shorten long URLs
- Redirect users using short codes
- Track clicks and creation date
- Thread-safe in-memory storage
- JSON-based persistence

---

## ⚡ Quickstart

### 1. **Clone the repository**

```bash
cd path/to/your/projects
git clone <repo-url>
cd url_shortener
```

### 2. **Install dependencies**

Ensure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 3. **Run the app**

```bash
python app/main.py
```

The service will start at:\
➡️ `http://localhost:5000/`

---

## 🧪 Run Tests

### Run `test_app.py`

```bash
cd tests
python test_app.py
```

### Run `concurrencytest_app.py`

```bash
cd tests
python concurrencytest_app.py
```

Make sure the main application is running on `http://localhost:5000` before running the concurrency test.

---

## 🛠 Project Structure

```
url_shortener/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── routes.py        # Api routes
│   ├── services.py      # Business logic
│   ├── storage.py       # In-memory
│   └── utils.py         # URL validation, hashing, encoding helpers
├── tests/
│   ├── test_app.py
│   └── concurrencytest_app.py
├── api_documentation.md
├── design_notes.md
└── README.md
```

---

## 📃 API Reference

See [`api_documentation.md`](./api_documentation.md) for full details.

Key Endpoints:

- `POST /api/shorten`
- `GET /<short_code>`
- `GET /api/stats/<short_code>`

---

