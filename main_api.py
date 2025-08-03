from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from logic import calc_pow, calc_fibonacci, calc_factorial

# ----- Config -----
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ----- App & Security -----
app = FastAPI()
auth_scheme = HTTPBearer()

# ----- Token logic -----
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

# ----- Fake login -----
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/token")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "password":
        token = create_access_token({"sub": data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# ----- Protected math endpoints -----
@app.get("/power")
def power(base: int, exp: int, user=Depends(verify_token)):
    return {"result": calc_pow(base, exp)}

@app.get("/factorial")
def factorial(n: int, user=Depends(verify_token)):
    return {"result": calc_factorial(n)}

@app.get("/fibonacci")
def fibonacci(n: int, user=Depends(verify_token)):
    return {"result": calc_fibonacci(n)}
