from elasticsearch import AsyncElasticsearch
from ..config import get_settings
import numpy as np, hashlib, asyncio, logging

settings = get_settings()
logger = logging.getLogger(__name__)

es = AsyncElasticsearch(hosts=settings.elastic_hosts.split(","))


async def _dummy_embed(text: str) -> list[float]:
    """Ejemplo: vector 384‑D basado en hash (reemplaza por tu modelo)."""
    h = hashlib.sha256(text.encode()).digest()
    return [b / 255 for b in h][:384]


async def upsert_embedding(doc_id: str, text: str):
    vector = await _dummy_embed(text)
    await es.index(
        index=settings.rag_index,
        id=doc_id,
        document={"text": text, "embedding": vector},
        refresh="wait_for"
    )
    logger.info("Indexed doc %s", doc_id)


async def hybrid_search(query: str, k: int = 5):
    body = {
        "size": k,
        "query": {
            "hybrid": {
                "queries": [
                    {"text": {"query": query}},
                    {"knn": {
                        "field": "embedding",
                        "query_vector_builder": {
                            "text_embedding": {
                                "model_id": "e5-small",
                                "model_text": query
                            }},
                        "k": k
                    }}
                ]
            }
        }
    }
    res = await es.search(index=settings.rag_index, body=body)
    return [{"doc_id": h["_id"], "score": h["_score"]} for h in res["hits"]["hits"]]
