import asyncio, logging
from ..services import cloudant, elastic

logger = logging.getLogger(__name__)

def _on_change(change):
    if change.get("deleted"):
        return
    doc = change["doc"]
    doc_id = doc["_id"]
    text = doc.get("content", "")
    # Ejecutamos la indexación en el event‑loop principal
    asyncio.run(elastic.upsert_embedding(doc_id, text))

async def start():
    """Lanza el follower en un hilo aparte para no bloquear FastAPI."""
    cloudant.spawn_changes_thread(_on_change)
    logger.info("Indexer started (changes follower)")
