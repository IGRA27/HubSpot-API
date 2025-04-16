from pydantic import BaseModel, Field
from typing import List, Optional

# ---------- Documentos ----------
class DocIn(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = Field(default_factory=list)

class DocOut(BaseModel):
    id: str

# ---------- Búsqueda ----------
class SearchHit(BaseModel):
    doc_id: str
    score: float

# ---------- CRM ----------
class ContactIn(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: Optional[str] = None

class ContactOut(BaseModel):
    id: str
    vid: int
