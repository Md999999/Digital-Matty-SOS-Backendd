from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

users = {}

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register")
def register(form: OAuth2PasswordRequestForm = Depends()):
    if form.username in users:
        raise HTTPException(status_code=400, detail="User exists")
    users[form.username] = form.password
    return {"message": "User registered"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form.username)
    if not user or user != form.password:
        raise HTTPException(status_code=400, detail="Wrong credentials")
    token = create_token(form.username)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you're authenticated!"}
