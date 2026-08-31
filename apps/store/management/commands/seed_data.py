from decimal import Decimal
import random

from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.products.models import Category, Products
from apps.store.models import Store, Inventory


fake = Faker()


class Command(BaseCommand):
    help = "Seed  data for the project(Category,Products,Inventory)"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Seeding data...")

        # -------------------------
        # Categories
        # -------------------------

        categories = [
            Category(name=f"Category {i}")
            for i in range(1, 11)
        ]

        Category.objects.bulk_create(
            categories,
            ignore_conflicts=True
        )

        categories = list(Category.objects.all())

        # -------------------------
        # Products
        # -------------------------

        products = [
            Products(
                title=f"{fake.word().title()} Product {i}",
                description=fake.text(max_nb_chars=200),
                price=Decimal(
                    str(round(random.uniform(10, 5000), 2))
                ),
                category=random.choice(categories)
            )
            for i in range(1, 1001)
        ]

        Products.objects.bulk_create(products)

        products = list(
            Products.objects.order_by("-id")[:1000]
        )

        # -------------------------
        # Stores
        # -------------------------

        stores = [
            Store(
                name=f"Store {i}",
                location=fake.city()
            )
            for i in range(1, 21)
        ]

        Store.objects.bulk_create(
            stores,
            ignore_conflicts=True
        )

        stores = list(Store.objects.all())

        # -------------------------
        # Inventory
        # -------------------------

        inventory = []

        for store in stores:
            selected_products = random.sample(
                products,
                300
            )

            for product in selected_products:
                inventory.append(
                    Inventory(
                        store=store,
                        product=product,
                        quantity=random.randint(0, 100)
                    )
                )

        Inventory.objects.bulk_create(inventory)

        self.stdout.write(
            self.style.SUCCESS(
                "Dummy data created successfully."
            )
        )