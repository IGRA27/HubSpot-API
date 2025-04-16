from hubspot import HubSpot
from hubspot.crm.contacts import ApiException as HubSpotApiException
from ..config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

hub = HubSpot(access_token=settings.hubspot_token)


async def create_or_update_contact(data: dict) -> dict:
    """Crea o actualiza contacto por e‑mail."""
    try:
        contact = hub.crm.contacts.basic_api.create(simple_public_object_input=data)
        return contact.to_dict()
    except HubSpotApiException as e:
        logger.error("HubSpot error: %s", e)
        raise
