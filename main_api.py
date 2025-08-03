import threading, queue, os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from logic import calc_pow, calc_fibonacci, calc_factorial
from database import save_request
from logging_config import setup_logging
import logging

setup_logging()

app = FastAPI()
auth_scheme = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-unsafe-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

q = queue.Queue()

class Task(BaseModel):
    operation: str
    params: dict

def worker():
    logging.info("[Worker] Worker thread started.")
    while True:
        task: Task = q.get()
        try:
            op = task.operation
            params = task.params
            if op == "power":
                result = calc_pow(**params)
            elif op == "factorial":
                result = calc_factorial(**params)
            elif op == "fibonacci":
                result = calc_fibonacci(**params)
            else:
                result = "invalid"
            save_request(op, str(params), str(result))
            logging.info(f"[Worker] {op}({params}) = {result}")
        except Exception as e:
            logging.error(f"[Worker] Error: {e}")
        q.task_done()

threading.Thread(target=worker, daemon=True).start()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/token")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "password":
        token = create_access_token({"sub": data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/power")
def power(base: int, exp: int, user=Depends(verify_token)):
    q.put(Task(operation="power", params={"base": base, "exp": exp}))
    return {"message": "Task submitted"}

@app.get("/factorial")
def factorial(n: int, user=Depends(verify_token)):
    q.put(Task(operation="factorial", params={"n": n}))
    return {"message": "Task submitted"}

@app.get("/fibonacci")
def fibonacci(n: int, user=Depends(verify_token)):
    q.put(Task(operation="fibonacci", params={"n": n}))
    return {"message": "Task submitted"}