from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from inventory_service.models import Product


class ProductApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            productName="Test pen",
            sku="PEN-001",
            color="Blue",
            size="M",
            isActive=True,
        )
        self.url = f"/api/v1/Products/{self.product.productId}"
        self.data = {
            "productName": "Test pen",
            "sku": "PEN-001",
            "color": "Blue",
            "size": "M",
            "isActive": True,
        }

    @patch("inventory_service.views.CdmsWebhookClient.send_product")
    def test_identical_put_keeps_product_data(self, mock_send_product):
        response = self.client.put(self.url, self.data, format="json")

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.color, "Blue")
        mock_send_product.assert_called_once()

    @patch("inventory_service.views.CdmsWebhookClient.send_product")
    def test_different_put_updates_product(self, mock_send_product):
        response = self.client.put(
            self.url,
            {**self.data, "color": "Red"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.color, "Red")
        mock_send_product.assert_called_once()
