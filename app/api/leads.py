# app/api/leads.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.lead import Lead

from app.schemas.lead import LeadCreate
from app.database import get_db
from app.services.lead_service import (
    get_all_leads,
    get_lead_by_id,
    create_lead,
    update_lead,
    delete_lead,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# List all leads
@router.get("/leads")
def list_leads(request: Request, db: Session = Depends(get_db)):
    leads = get_all_leads(db)
    return templates.TemplateResponse("leads/list.html", {"request": request, "leads": leads})


# Show form to add a new lead
@router.get("/leads/add")
def show_add_lead_form(request: Request):
    return templates.TemplateResponse("leads/add.html", {"request": request})


# Handle form submission for adding a lead
@router.post("/leads/add")
def add_lead(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    lead_data = LeadCreate(name=name, email=email, phone=phone)
    create_lead(db, lead_data)
    return templates.TemplateResponse(
        "leads/add.html",
        {
            "request": request,
            "message": "Lead added successfully!",
            "lead": lead_data,
        },
    )


# View details of a specific lead
@router.get("/leads/{lead_id}")
def lead_detail(request: Request, lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return templates.TemplateResponse("leads/detail.html", {"request": request, "lead": lead})


# GET route to show the edit form
@router.get("/leads/{lead_id}/edit")
def edit_lead_form(request: Request, lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return templates.TemplateResponse("leads/edit.html", {"request": request, "lead": lead})


# POST route to update the lead
@router.post("/leads/{lead_id}/edit")
def update_lead_post(
    request: Request,
    lead_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    db: Session = Depends(get_db),
):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead_data = LeadCreate(name=name, email=email, phone=phone)
    update_lead(db, lead_id, lead_data)

    return RedirectResponse(url=f"/leads/{lead_id}", status_code=303)

@router.get("/leads/{lead_id}/delete")
def confirm_delete_lead(request: Request, lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return templates.TemplateResponse("leads/confirm_delete.html", {"request": request, "lead": lead})

@router.post("/leads/{lead_id}/delete")
def delete_lead_post(lead_id: int, db: Session = Depends(get_db)):
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    delete_lead(db, lead)
    return RedirectResponse(url="/leads", status_code=303)


