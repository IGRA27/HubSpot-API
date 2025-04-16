from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from ..services import cloudant, elastic
from ..models import DocIn, DocOut

router = APIRouter(prefix="/docs", tags=["documents"])

@router.post("/", response_model=DocOut, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocIn, background_tasks: BackgroundTasks):
    doc_id = await cloudant.save_doc(doc.dict())
    # indexamos en segundo plano usando BackgroundTasks (no bloquea la respuesta)
    background_tasks.add_task(elastic.upsert_embedding, doc_id, doc.content)
    return DocOut(id=doc_id)

@router.get("/{doc_id}", response_model=DocIn)
async def read_document(doc_id: str):
    try:
        return await cloudant.get_doc(doc_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Not found")
