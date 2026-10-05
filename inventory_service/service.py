from django.db.models import QuerySet
from inventory_service.repositories import ProductRepository
from rest_framework.exceptions import NotFound
from inventory_service.models import Product
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