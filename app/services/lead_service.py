# app/services/lead_service.py

from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def get_all_leads(db: Session):
    return db.query(Lead).all()


def get_lead_by_id(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()


def create_lead(db: Session, lead_data: LeadCreate):
    lead = Lead(
        name=lead_data.name,
        email=lead_data.email,
        phone=lead_data.phone,
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Lead with this email already exists")

    db.refresh(lead)
    return lead

def update_lead(db: Session, lead_id: int, lead_data: LeadCreate): 
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None
    lead.name = lead_data.name
    lead.email = lead_data.email
    lead.phone = lead_data.phone
    db.commit()
    db.refresh(lead)
    return lead

def delete_lead(db: Session, lead: Lead):
    db.delete(lead)
    db.commit()

