from fastapi import APIRouter, HTTPException, status
from ..services.hubspot import create_or_update_contact
from ..models import ContactIn, ContactOut

router = APIRouter(prefix="/crm", tags=["crm"])

@router.post("/contacts", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
async def upsert_contact(contact: ContactIn):
    try:
        res = await create_or_update_contact(contact.dict())
        return ContactOut(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
