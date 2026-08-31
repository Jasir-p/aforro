# tests/conftest.py

import pytest

from apps.products.models import Category, Products
from apps.store.models import Store, Inventory


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Electronics"
    )


@pytest.fixture
def product(db, category):
    return Products.objects.create(
        title="iPhone",
        description="Smart phone",
        price=50000,
        category=category
    )


@pytest.fixture
def store(db):
    return Store.objects.create(
        name="Test Store",
        location="Kochi"
    )


@pytest.fixture
def inventory(db, store, product):
    return Inventory.objects.create(
        store=store,
        product=product,
        quantity=10
    )