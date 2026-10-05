import requests
from django.conf import settings


class InventoryClient:
    """Fetch product snapshots from the emulated Inventory Service."""

    def list_products(self) -> list[dict]:
        response = requests.get(
            settings.CDMS_INVENTORY_PRODUCTS_URL,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
