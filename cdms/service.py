from django.db import IntegrityError, transaction

from cdms.models import ManagedProduct
from cdms.repositories import ManagedProductRepository


class CdmsService:
    def __init__(self):
        self.repository = ManagedProductRepository()

    def sync_product(
        self,
        product_data: dict,
    ) -> tuple[ManagedProduct, bool]:
        product_id = product_data["productId"]

        with transaction.atomic():
            managed_product = self.repository.get_by_product_id_for_update(
                product_id=product_id
            )

            if managed_product is None:
                try:
                    with transaction.atomic():
                        created_product = self.repository.create(
                            product_id=product_id,
                            product_data=product_data,
                        )
                    return created_product, True
                except IntegrityError:
                    # Another concurrent request created this product first.
                    managed_product = self.repository.get_by_product_id_for_update(
                        product_id=product_id
                    )

            if managed_product.product_data == product_data:
                return managed_product, False

            updated_product = self.repository.update(
                managed_product=managed_product,
                product_data=product_data,
            )
            return updated_product, True
