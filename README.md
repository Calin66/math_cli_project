# Math CLI Tool

A Python command-line application that performs simple mathematical operations and saves each request to an SQLite database. 

## Features

- CLI built with `click`
- Operations: power, factorial, Fibonacci
- Input validation with `pydantic`
- Background processing using `threading` and `queue`
- Request logging in `SQLite`
- Clean structure and flake8-compliant

## Project Structure

math_cli_project/
├── cli.py
├── logic.py
├── models.py
├── database.py
├── queue_handler.py
├── requirements.txt
├── .flake8

## Usage

1. Create and activate virtual environment
```
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux
```

2. Install requirements
```
pip install -r requirements.txt
```

3. Run commands
```
python cli.py power --base 2 --exp 5
python cli.py factorial --n 5
python cli.py fibonacci --n 10
```

## Notes

- Each command adds a task to a background worker via a queue
- The worker calculates the result and stores it in `requests.db`
- A shutdown signal is sent after each command to stop the worker cleanly
