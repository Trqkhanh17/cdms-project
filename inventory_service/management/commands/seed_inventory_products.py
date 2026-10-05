from django.core.management.base import BaseCommand
from faker import Faker

from inventory_service.models import Product


class Command(BaseCommand):
    help = "Create fake Inventory products for local demos and spike tests."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        count = options["count"]
        faker = Faker()
        products = [
            Product(
                productName=faker.catch_phrase()[:255],
                sku=faker.unique.bothify(text="SKU-####??"),
                color=faker.safe_color_name(),
                size=faker.random_element(["S", "M", "L", "XL"]),
                isActive=faker.boolean(chance_of_getting_true=90),
            )
            for _ in range(count)
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f"Created {count} fake products."))
