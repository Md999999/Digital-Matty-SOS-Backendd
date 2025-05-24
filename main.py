from fastapi import FastAPI
from app import auth, routes

app = FastAPI(
    title="SOS Alert System",
    description="Backend for emergency contacts and alerts",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(routes.router)

