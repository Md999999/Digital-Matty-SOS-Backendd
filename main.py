from fastapi import FastAPI
from app import auth, routes

app = FastAPI()

app.include_router(auth.router)
app.include_router(routes.router)

