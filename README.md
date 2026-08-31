# AFORRO Backend API

A Django REST Framework backend for managing products, stores, inventory, product search, suggestions, and order processing.

The project is containerized with Docker and uses PostgreSQL for database management, Redis for caching, and Celery for asynchronous task processing.

---

## Features

* Product and category management
* Store management
* Store-wise inventory management
* Product search
* Product filtering
* Product sorting
* Product autocomplete suggestions
* Redis caching for search suggestions
* Order creation
* Inventory/stock validation during order creation
* `CONFIRMED` and `REJECTED` order statuses
* Inventory update after confirmed orders
* Store-wise order listing
* Store-wise inventory listing
* Seed data management command
* Celery task integration
* PostgreSQL database
* Redis
* Docker environment
* Pytest automated tests
* Swagger/OpenAPI documentation
* Postman API collection

---

# Technology Stack

| Technology            | Purpose                       |
| --------------------- | ----------------------------- |
| Python                | Backend programming           |
| Django                | Web framework                 |
| Django REST Framework | REST API                      |
| PostgreSQL            | Relational database           |
| Redis                 | Caching and Celery broker     |
| Celery                | Background task processing    |
| Docker                | Containerization              |
| Pytest                | Automated testing             |
| pytest-django         | Django test integration       |
| Faker                 | Seed data generation          |
| drf-spectacular       | Swagger/OpenAPI documentation |

---

# Project Structure

```text
aforro-backend/
│
├── apps/
│   ├── products/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── stores/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── orders/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tasks.py
│   │   └── ...
│   │
│   └── search/
│       ├── views.py
│       ├── services.py
│       ├── urls.py
│       └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── ...
│
├── tests/
│   ├── test_orders.py
│   ├── test_products_search.py
│   └── ...
│
├── postman/
│   └── AFORRO.postman_collection.json
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pytest.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Requirements

The project is designed to run using Docker.

You need:

* Docker
* Docker Compose
* Git

PostgreSQL and Redis can run through the provided Docker environment.

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd aforro-backend
```

---

## 2. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DEBUG=True

POSTGRES_DB=aforro
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CACHE_REDIS_URL=redis://redis:6379/2

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

Do not commit sensitive production credentials to GitHub.

---

# Docker

## Start the Application

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

---

# Database Migration

Run Django migrations:

```bash
docker exec -it django-docker python manage.py migrate
```

---

# Seed Data

The project includes a Django management command for populating the database with sample data.

Run:

```bash
docker exec -it django-docker python manage.py seed_data
```

The seed command creates sample data required for API testing, such as:

* Categories
* Products
* Stores
* Inventory records

Run migrations before running the seed command.

---

# API Documentation

The project uses `drf-spectacular` for OpenAPI documentation.

## Swagger UI

```text
http://localhost:8000/api/schema/swagger-ui/
```

Swagger provides an interactive interface for viewing and testing the APIs.

## OpenAPI Schema

```text
http://localhost:8000/api/schema/
```

## ReDoc

```text
http://localhost:8000/api/schema/redoc/
```

---

# API Endpoints

## Orders

### Create Order

```http
POST /api/orders/
```

### Request

```json
{
    "store_id": 1,
    "items": [
        {
            "product_id": 23,
            "quantity_requested": 2
        }
    ]
}
```

### Order Processing

If sufficient stock is available:

```text
CONFIRMED
```

The inventory quantity is reduced by the requested quantity.

If the requested quantity exceeds available stock:

```text
REJECTED
```

The inventory quantity remains unchanged.

### Example

If:

```text
Stock = 10
Requested = 5
```

Result:

```text
CONFIRMED
Remaining Stock = 5
```

If:

```text
Stock = 10
Requested = 20
```

Result:

```text
REJECTED
Remaining Stock = 10
```

---

## List Store Orders

```http
GET /api/stores/{store_id}/orders/
```

Example:

```http
GET /api/stores/1/orders/
```

Returns orders associated with the specified store.

---

# Inventory

## List Store Inventory

```http
GET /api/stores/{store_id}/inventory/
```

Example:

```http
GET /api/stores/1/inventory/
```

Returns inventory information for the specified store.

---

# Product Search

## Search Products

```http
GET /api/search/products/
```

### Basic Search

```http
GET /api/search/products/?q=phone
```

### Search by Store

```http
GET /api/search/products/?q=phone&store_id=1
```

### Search with Sorting

```http
GET /api/search/products/?q=phone&sort=price
```

### Search with Multiple Parameters

```http
GET /api/search/products/?q=phone&sort=price&store_id=1
```

### Query Parameters

| Parameter   | Description                        |
| ----------- | ---------------------------------- |
| `q`         | Product search keyword             |
| `category`  | Filter products by category        |
| `min_price` | Minimum price                      |
| `max_price` | Maximum price                      |
| `store_id`  | Filter products based on store     |
| `in_stock`  | Filter based on stock availability |
| `sort`      | Sort search results                |
| `page`      | Pagination page                    |
| `page_size` | Number of results per page         |

Example:

```http
GET /api/search/products/?q=phone&category=1&min_price=100&max_price=50000&store_id=1&in_stock=true&sort=price
```

---

# Product Suggestions

## Search Suggestions

```http
GET /api/search/suggest/
```

Example:

```http
GET /api/search/suggest/?q=iph
```

Returns product suggestions matching the provided search prefix.

---

# Redis Caching

Redis is used to cache frequently requested product search suggestions.

When the same suggestion query is requested repeatedly, the cached result can be returned from Redis instead of querying the database again.

### Benefits

* Reduces repeated database queries
* Improves response time
* Reduces database workload
* Helps handle frequent autocomplete requests

Redis is also used as the infrastructure for Celery.

---

# Celery

Celery is integrated into the project for asynchronous/background task processing.

Redis is used as the Celery message broker and result backend.

## Example Task: Order Confirmation Notification

When an order is created and confirmed, a Celery task is dispatched to handle notification/logging work asynchronously instead of blocking the API response.

### Task

`apps/orders/tasks.py`

```python
from celery import shared_task


@shared_task
def send_order_confirmation(order_id):
    from apps.orders.models import Order

    order = Order.objects.get(id=order_id)

    # Example background notification/logging operation
    print(f"Order {order.id} confirmed. Notification sent.")

    return order.id
```

### Triggering the Task

After a confirmed order is created:

```python
if order.status == "CONFIRMED":
    send_order_confirmation.delay(order.id)
```

The `.delay()` method sends the task to Celery instead of executing it synchronously inside the API request.

### Verifying the Task

Check the Celery worker logs:

```bash
docker compose logs -f celery
```

After creating a confirmed order, the Celery worker should receive and execute the task.

### Why Use Celery?

Notification or logging operations are not required to determine the order result.

Running these operations asynchronously:

* Keeps the order API response fast
* Prevents notification I/O from blocking the request
* Allows background tasks to be processed independently
* Makes the system easier to scale

---

# Redis Database Separation

Different Redis databases are used for different purposes:

```text
Redis DB 0
    └── Celery Broker

Redis DB 1
    └── Celery Result Backend

Redis DB 2
    └── Django Application Cache
```

This keeps application cache data separate from Celery messaging and task results.

---

# Order and Inventory Consistency

Order creation validates the requested quantity against available inventory.

The order and inventory operation is handled using a database transaction so that the order and stock update remain consistent.

### Confirmed Order

```text
Available Stock
       ↓
Check requested quantity
       ↓
Sufficient
       ↓
Create CONFIRMED order
       ↓
Reduce inventory
```

### Rejected Order

```text
Available Stock
       ↓
Check requested quantity
       ↓
Insufficient
       ↓
Create REJECTED order
       ↓
Do not reduce inventory
```

For high-concurrency production workloads, row-level locking such as `select_for_update()` can be used to prevent simultaneous orders from consuming the same stock.

---

# Testing

The project uses Pytest and pytest-django for automated testing.

## Run All Tests

```bash
docker exec -it django-docker pytest -v
```

## Run Order Tests

```bash
docker exec -it django-docker pytest tests/test_orders.py -v
```

## Run Product Search Tests

```bash
docker exec -it django-docker pytest tests/test_products_search.py -v
```

The tests automatically create and use a separate test database, so they do not modify the development database.

## Test Coverage

The test suite covers important scenarios including:

* Confirmed order creation
* Rejected order when stock is insufficient
* Inventory quantity validation
* Product search by title
* API response/status validation

---

# Postman Collection

The Postman collection is included in:

```text
postman/AFORRO.postman_collection.json
```

## Collection Structure

```text
AFORRO
│
├── orders
│   ├── create order
│   └── list-store-order
│
├── inventory
│   └── list-store-inventory
│
└── search
    ├── product-search
    └── search-suggest
```

---

# Using Postman

Start the application:

```bash
docker compose up -d --build
```

Run migrations:

```bash
docker exec -it django-docker python manage.py migrate
```

Generate seed data:

```bash
docker exec -it django-docker python manage.py seed_data
```

Open Postman and import:

```text
postman/AFORRO.postman_collection.json
```

The collection uses:

```text
http://localhost:8000
```

---

# Sample Postman Requests

## Create Order

```http
POST http://localhost:8000/api/orders/
```

Body:

```json
{
    "store_id": 1,
    "items": [
        {
            "product_id": 23,
            "quantity_requested": 2
        }
    ]
}
```

---

## List Store Orders

```http
GET http://localhost:8000/api/stores/1/orders/
```

---

## List Store Inventory

```http
GET http://localhost:8000/api/stores/1/inventory/
```

---

## Product Search

```http
GET http://localhost:8000/api/search/products/?q=phone&sort=price&store_id=1
```

---

## Product Suggestion

```http
GET http://localhost:8000/api/search/suggest/?q=iph
```

---

# Scalability Considerations

## Database

PostgreSQL is used as the primary database.

For larger datasets:

* Add indexes to frequently searched fields
* Optimize ORM queries
* Use `select_related()` and `prefetch_related()`
* Use database constraints for data integrity
* Use transactions for operations involving multiple database updates

## Redis

Redis caching reduces repeated database queries for frequently requested search suggestions.

The same approach can be extended to other frequently accessed and relatively stable data.

## Celery

Celery workers can be scaled independently from Django.

Additional Celery workers can be added as asynchronous workloads increase.

## Search Scalability

For a significantly larger product catalog, a dedicated search engine such as Elasticsearch or OpenSearch could be introduced for:

* Full-text search
* Autocomplete
* Relevance ranking
* Advanced filtering
* High-volume search traffic

## Inventory Concurrency

For high-volume order processing, inventory updates should use appropriate transaction isolation and row-level locking.

For example:

```python
transaction.atomic()
select_for_update()
```

This helps prevent simultaneous requests from consuming the same inventory.

---

# Useful Docker Commands

## Start

```bash
docker compose up -d --build
```

## Stop

```bash
docker compose down
```

## Check Containers

```bash
docker compose ps
```

## Django Logs

```bash
docker compose logs -f django-docker
```

## Run Migrations

```bash
docker exec -it django-docker python manage.py migrate
```

## Seed Data

```bash
docker exec -it django-docker python manage.py seed_data
```

## Django Shell

```bash
docker exec -it django-docker python manage.py shell
```

## Run Tests

```bash
docker exec -it django-docker pytest -v
```

---

# Complete Setup and Testing Flow

A reviewer can follow these steps:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd aforro-backend

docker compose up -d --build

docker exec -it django-docker python manage.py migrate

docker exec -it django-docker python manage.py seed_data

docker exec -it django-docker pytest -v
```

Then open Swagger:

```text
http://localhost:8000/api/schema/swagger-ui/
```

Or import the Postman collection:

```text
postman/AFORRO.postman_collection.json
```

---

# Recommended API Testing Flow

```text
Start Docker
     ↓
Run migrations
     ↓
Run seed_data
     ↓
Run automated tests
     ↓
Open Swagger / Import Postman
     ↓
Test Product Search
     ↓
Test Product Suggestions
     ↓
Test Store Inventory
     ↓
Create Confirmed Order
     ↓
Verify Inventory Reduction
     ↓
Create Rejected Order
     ↓
Verify Inventory Remains Unchanged
     ↓
List Store Orders
```

---

# Submission Checklist

* [x] Complete Django project
* [x] Required models
* [x] REST APIs
* [x] Serializers
* [x] URL configuration
* [x] Seed data management command
* [x] PostgreSQL database
* [x] Redis caching
* [x] Celery integration
* [x] Docker environment
* [x] 3–5+ automated tests
* [x] Swagger/OpenAPI documentation
* [x] Postman collection
* [x] Setup instructions
* [x] Docker usage instructions
* [x] Sample API requests
* [x] Caching/async processing notes
* [x] Scalability considerations

---

# Conclusion

This project demonstrates a containerized Django REST API with product search, store-wise inventory, order processing, Redis caching, Celery integration, automated testing, Swagger/OpenAPI documentation, and Postman-based API testing.

The architecture provides a foundation that can be extended for higher traffic, larger datasets, and additional background processing requirements.
