from django.db.models import QuerySet
from inventory_service.repositories import ProductRepository
from rest_framework.exceptions import NotFound
from inventory_service.models import Product
from django.db import transaction
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def list_products(self)-> QuerySet[Product]:
        return self.repository.list_products()
    
    def get_product(self,product_id)->Product:
        product = self.repository.get_product_by_id(product_id)
        if product is None:
            raise NotFound("Product Not Found")
        return product
    
    def create_product(self, product_data:dict)->Product:
        with transaction.atomic():
            return self.repository.create_product(product_data)

    def update_product(self, product: Product, product_data: dict) -> Product:
        with transaction.atomic():
            for field, value in product_data.items():
                if getattr(product, field) != value:
                    return self.repository.update_product(product, product_data)

            return product
