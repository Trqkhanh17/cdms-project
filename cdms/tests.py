from io import BytesIO
from unittest.mock import patch

from django.test import TestCase
from openpyxl import Workbook
from rest_framework.test import APIClient

from cdms.models import ManagedProduct
from cdms.service import CdmsService


class CdmsServiceTests(TestCase):
    def setUp(self):
        self.service = CdmsService()
        self.blue_product = {
            "productId": 1,
            "productName": "Test pen",
            "sku": "PEN-001",
            "color": "Blue",
            "size": "M",
            "isActive": True,
        }

    def test_create_duplicate_then_update(self):
        managed_product, changed = self.service.sync_product(self.blue_product)
        self.assertTrue(changed)
        self.assertEqual(managed_product.product_data, self.blue_product)
        self.assertEqual(ManagedProduct.objects.count(), 1)

        _, changed = self.service.sync_product(self.blue_product)
        self.assertFalse(changed)
        self.assertEqual(ManagedProduct.objects.count(), 1)

        red_product = {**self.blue_product, "color": "Red"}
        managed_product, changed = self.service.sync_product(red_product)
        self.assertTrue(changed)
        self.assertEqual(managed_product.product_data, red_product)
        self.assertEqual(ManagedProduct.objects.count(), 1)


class WebhookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = {
            "productId": 2,
            "productName": "Webhook pen",
            "color": "Blue",
            "isActive": True,
        }

    def test_webhook_reports_duplicate_data(self):
        first_response = self.client.post(
            "/api/v1/webhooks/products",
            self.product,
            format="json",
        )
        duplicate_response = self.client.post(
            "/api/v1/webhooks/products",
            self.product,
            format="json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.data["changed"])
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertFalse(duplicate_response.data["changed"])

    @patch("cdms.scheduled_sync.InventoryClient.list_products")
    def test_scheduled_sync_processes_inventory_snapshots(self, mock_list_products):
        mock_list_products.return_value = [self.product]

        response = self.client.post("/api/v1/scheduled-sync", format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"changed": 1, "unchanged": 0})

    def test_excel_upload_processes_product_rows(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(
            ["productId", "productName", "sku", "color", "size", "isActive"]
        )
        worksheet.append([3, "Excel pen", "PEN-003", "Green", "L", True])
        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)
        stream.name = "products.xlsx"

        response = self.client.post(
            "/api/v1/uploads/products",
            {"file": stream},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["changed"], 1)
        self.assertEqual(response.data["errors"], [])
