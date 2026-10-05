import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class CdmsWebhookClient:
    """Push a product snapshot to the CDMS webhook."""

    def send_product(self, product_data: dict) -> bool:
        try:
            response = requests.post(
                settings.CDMS_WEBHOOK_URL,
                json=product_data,
                timeout=5,
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            logger.exception("Could not deliver product snapshot to CDMS")
            return False
