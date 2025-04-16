from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibmcloudant.features.changes_follower import ChangesFollower, Mode
from ..config import get_settings
import logging, threading

settings = get_settings()
logger = logging.getLogger(__name__)

client = CloudantV1.new_instance(
    url=settings.cloudant_url,
    authenticator={"apikey": settings.cloudant_api_key}
)
DB = settings.db_name


async def save_doc(payload: dict) -> str:
    res = client.post_document(db=DB, document=Document(**payload)).get_result()
    return res["id"]


async def get_doc(doc_id: str) -> dict:
    return client.get_document(db=DB, doc_id=doc_id).get_result()


def follow_changes(callback):
    """Ejecuta un seguidor de cambios (hilo bloqueante)."""
    follower = ChangesFollower(
        client,
        db=DB,
        mode=Mode.continuous,
        include_docs=True,
        since="now",
        callback=callback
    )
    follower.start()
    follower.join()          # mantiene el hilo vivo


def spawn_changes_thread(callback):
    thread = threading.Thread(target=follow_changes, args=(callback,), daemon=True)
    thread.start()
    logger.info("Changes follower thread started")
