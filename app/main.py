# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.api import leads, dashboard

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(dashboard.router, prefix="", tags=["dashboard"])
app.include_router(leads.router, prefix="", tags=["leads"])
