# Math CLI & API Toolkit

A Python-based project offering both a command-line interface (CLI) and a REST web API for basic math operations: power, factorial, and Fibonacci. Includes features such as caching, logging, automated testing, containerization, and authentication.

---

## Features

- CLI interface using `click`
- Operations: `power`, `factorial`, `fibonacci`
- Input validation with `pydantic`
- In-memory caching
- Structured logging (to file and console)
- SQLite database logging (`requests.db`)
- Unit testing with `pytest`
- REST API via `FastAPI` with token authentication
- Minimal HTML UI for testing
- Dockerized CLI usage

---

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate         # Linux/macOS
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## CLI Usage

```bash
python cli.py power --base 2 --exp 5
python cli.py factorial --n 5
python cli.py fibonacci --n 10
```

The result is:
- Printed to console
- Logged to `app.log`
- Stored in `requests.db`
- Cached if called again with same inputs

---

## Testing

```bash
pytest
```

Tests in `test_logic.py` ensure each math function works correctly.

---

## FastAPI REST API

### 1. Start the API server

```bash
uvicorn main_api:app --reload
```

### 2. Open Swagger documentation

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Authentication

All endpoints require a token:

```
Authorization: Bearer secret123
```

### 4. Example `curl` request

```bash
curl -X GET "http://127.0.0.1:8000/power?base=2&exp=5" ^
     -H "Authorization: Bearer secret123"
```

---

## HTML Frontend

1. Open `frontend.html` in your browser
2. Fill in values
3. Submit the form

*Note: This form does not include token authentication.*

---

## Docker

### 1. Build the image

```bash
docker build -t math-cli .
```

### 2. Run CLI in container

```bash
docker run math-cli python cli.py power --base 2 --exp 5
```

---

## Project Structure

```
math_cli_project/
├── cli.py
├── logic.py
├── models.py
├── database.py
├── queue_handler.py
├── main_api.py
├── frontend.html
├── logging_config.py
├── test_logic.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Token

Static token for API authentication:

```
secret123
```

---


## JWT Authentication

### 1. Get a token

Send a POST request to:

```
POST /token
```

With JSON body:
```json
{
  "username": "admin",
  "password": "password"
}
```

If valid, you'll receive:
```json
{
  "access_token": "<JWT token>",
  "token_type": "bearer"
}
```

### 2. Use the token

Include it in requests to protected endpoints:
```
Authorization: Bearer <token>
```

Example with `curl`:
```bash
curl -X GET "http://127.0.0.1:8000/power?base=2&exp=5" \
     -H "Authorization: Bearer <your-token>"
```

The token is valid for 30 minutes by default.
