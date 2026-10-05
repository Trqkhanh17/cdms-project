from django.db import models


class Product(models.Model):
    productId = models.BigAutoField(primary_key=True, help_text='unique ID of product')
    productName = models.CharField(max_length = 255, null= True, blank = True, help_text='Name of product')
    sku = models.CharField(max_length=100, blank=True, null=True, help_text='sku of product')
    color = models.CharField(max_length=50, blank=True, null=True, help_text='color of product')
    size = models.CharField(max_length=50, blank=True, null=True, help_text='size of product')
    isActive = models.BooleanField(default=True, help_text = 'is active product')
    class Meta:
        ordering = ['productId']

    def __str__(self):
        return f"{self.productId} - {self.productName or self.sku or 'Unnamed product'}"