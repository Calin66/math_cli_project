# Multithreaded CLI & API Math Microservice

A Python project that offers both a CLI tool and a REST API for computing power, factorial, and Fibonacci using multithreading and background task queues. Includes JWT authentication, SQLite storage, logging, Docker support, and automated testing.

## Features
- CLI via `click`
- REST API via `FastAPI`
- JWT-based authentication
- Caching and SQLite logging
- Multithreaded async processing
- Docker-ready deployment
- Automated tests with `pytest`

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on cmd
pip install -r requirements.txt
```

## Usage (CLI)
```bash
python cli.py power --base 2 --exp 5
```

## Usage (API)
Start the server:
```bash
uvicorn main_api:app --reload
```
Then:
1. Get a token from `http://127.0.0.1:8000/docs/` expand /token, use:
```json
{ "username": "admin", "password": "password" }
```
or

```bash
curl -X POST http://127.0.0.1:8000/token -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"password\"}"
```

2. Call `/power`, `/factorial`, or `/fibonacci` with the token and check app.log or requests.db.

```bash
curl -X GET "http://127.0.0.1:8000/power?base=2&exp=5" -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Docker
```bash
docker build -t math-cli .
docker run -e SECRET_KEY=your_key_here math-cli
```

## Testing
```bash
pytest
```