from .models import Order, OrderItem
from django.db import transaction
from apps.store.models import Inventory
from .tasks import send_order_confirmation
from django.db.models import Count



#Get Inventories from   given store
def get_store_inventory(store_id, product_ids):

    return (Inventory.objects.select_for_update().select_related("product").filter(
        store=store_id,
        product_id__in=product_ids
    ))


#check stock if available in given inventries
def check_stock(inventories,items):
    inventory_dict = {
        inventory.product_id:inventory
        for inventory in inventories
    }

    for item in items:
        inventory = inventory_dict.get(item['product_id'])

        if not inventory:
            return False

        if inventory.quantity < item["quantity_requested"]:
            return False

    return True


#create orderitems
def create_order_items(order,items):
    order_items = [
        OrderItem(
            order=order,
            product_id = item['product_id'],
            quantity_requested=item["quantity_requested"]
        )

        for item in items
    ]

    return OrderItem.objects.bulk_create(order_items)


def deduct_inventory_stock(inventories,items):
    inventory_dict = {
        inventory.product_id: inventory
        for inventory in inventories
    }

    for item in items:
        inventory = inventory_dict[item['product_id']]
        inventory.quantity -= item["quantity_requested"]
        inventory.save()


@transaction.atomic()
def create_order(store_id,items):
    product_ids = [
        item["product_id"]
        for item in items
    ]

    inventories = get_store_inventory(store_id,product_ids)

    is_stock = check_stock(inventories,items)

    if is_stock:
        order_status = "CONFIRMED"
    else:
        order_status = "REJECTED"

    order = Order.objects.create(
        store_id=store_id,
        status=order_status

    )
    create_order_items(
        order, items
        )

    if is_stock:
        deduct_inventory_stock(
            inventories, items
        )
    transaction.on_commit(
        lambda: send_order_confirmation.delay(order.id)
        )
    return order




def get_store_orders(store_id):
    return Order.objects.filter(
        store_id=store_id
    ).annotate(
        total_items=Count("items")
    ).order_by("-created_at")