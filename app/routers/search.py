from fastapi import APIRouter, Query
from ..services.elastic import hybrid_search
from ..models import SearchHit
from typing import List

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/", response_model=List[SearchHit])
async def search(q: str = Query(..., min_length=3), k: int = 5):
    return await hybrid_search(q, k)
