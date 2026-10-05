from django.db import models


class ManagedProduct(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    product_data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Managed product: {self.product_id}"
