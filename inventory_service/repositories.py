from django.db.models import QuerySet

from inventory_service.models import Product


class ProductRepository:
    def list_products(self) -> QuerySet[Product]:
        return Product.objects.all()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return Product.objects.filter(
            productId=product_id
        ).first()

    def create_product(self, product_data:dict) -> Product:
        return Product.objects.create(**product_data)

    def update_product(self,product:Product, product_data:dict) -> Product:
        for field, value in product_data.items():
            setattr(product,field,value)
        product.save()
        return product