import logging

from cdms.clients.inventory_client import InventoryClient
from cdms.service import CdmsService


logger = logging.getLogger(__name__)


class ScheduledInventorySync:
    """One scheduled pull from Inventory, followed by CDMS processing."""

    def __init__(self):
        self.inventory_client = InventoryClient()
        self.cdms_service = CdmsService()

    def run_once(self) -> dict[str, int]:
        created_or_updated = 0
        unchanged = 0

        for product_data in self.inventory_client.list_products():
            _, changed = self.cdms_service.sync_product(product_data)
            if changed:
                created_or_updated += 1
            else:
                unchanged += 1

        result = {
            "changed": created_or_updated,
            "unchanged": unchanged,
        }
        logger.info("Scheduled inventory sync completed: %s", result)
        return result
