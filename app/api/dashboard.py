# app/api/dashboard.py

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
