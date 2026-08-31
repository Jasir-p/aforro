import pytest

from rest_framework.test import APIClient

from apps.products.models import Category, Products
from apps.store.models import Store, Inventory


@pytest.fixture
def client():
    return APIClient()


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



@pytest.mark.django_db
class TestOrder:

    def test_create_order_confirmed(self,client,store,product,inventory):
        payload = {
            "store_id": store.id,
            "items": [
                {
                    "product_id": product.id,
                    "quantity_requested": 5
                }
            ]
        }

        response = client.post(
            "/api/orders/",
            payload,
            format="json"
        )

        assert response.status_code == 201
        assert response.data["status"] == "CONFIRMED"

        inventory.refresh_from_db()

        assert inventory.quantity == 5


    def test_create_order_rejected(self,client,store,product,inventory):
            payload = {
                "store_id": store.id,
                "items": [
                    {
                        "product_id": product.id,
                        "quantity_requested": 20
                    }
                ]
            }
    
            response = client.post(
                "/api/orders/",
                payload,
                format="json"
            )
    
            assert response.status_code == 201
            assert response.data["status"] == "REJECTED"
    
            inventory.refresh_from_db()
    
            assert inventory.quantity == 10


    def test_create_order_stockout(
        self,
        client,
        store,
        product,
        inventory
    ):
        inventory.quantity = 0
        inventory.save()

        payload = {
            "store_id": store.id,
            "items": [
                {
                    "product_id": product.id,
                    "quantity_requested": 1
                }
            ]
        }

        response = client.post(
            "/api/orders/",
            payload,
            format="json"
        )

        assert response.status_code == 201
        assert response.data["status"] == "REJECTED"

        inventory.refresh_from_db()

        assert inventory.quantity == 0