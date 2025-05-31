# app/schemas/lead.py

from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int

    class Config:
        orm_mode = True
