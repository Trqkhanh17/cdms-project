# Change Data Management Service Prototype

This project emulates a small Inventory Service and a Change Data Management
Service (CDMS) in one Django project. PostgreSQL stores both logical databases.

## Architecture

`inventory_service.Product` is the Inventory database. `cdms.ManagedProduct` is
the Change Database. CDMS receives a full Product snapshot and applies one rule:

1. no matching `product_id`: create a managed Product;
2. matching JSON: do nothing;
3. different JSON: update the managed Product.

`ManagedProduct.product_id` is unique, so CDMS stores at most one current
snapshot for each Inventory Product and does not retain old values.

## Data ingestion mechanisms

| Mechanism | Entry point | How to run |
| --- | --- | --- |
| Webhook callback | `POST /api/v1/webhooks/products` | Inventory POST/PUT sends the current Product snapshot automatically. |
| Scheduled query | `CdmsService` via `InventoryClient` | `python manage.py run_cdms_scheduler --once` or run continuously without `--once`. |
| Excel REST upload | `POST /api/v1/uploads/products` | Multipart field name: `file`; accepts `.xlsx`. |

The workbook's first row must use these headers: `productId`, `productName`,
`sku`, `color`, `size`, `isActive`.

## Local setup

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker compose up -d postgres
python manage.py migrate
python manage.py runserver
```

Create sample Inventory data:

```bash
python manage.py seed_inventory_products 100
```

Run one scheduled query:

```bash
python manage.py run_cdms_scheduler --once
```

Run all services in containers:

```bash
docker compose up --build
```

## Product API

| Method | URL | Purpose |
| --- | --- | --- |
| GET | `/api/v1/Products` | List Inventory Products |
| POST | `/api/v1/Products` | Create Inventory Product and send a webhook snapshot |
| GET | `/api/v1/Products/<id>` | Read one Product |
| PUT | `/api/v1/Products/<id>` | Update only when input is different, then send a webhook snapshot |

## Failure handling and recovery

The callback client uses a five-second timeout and logs failed webhook delivery.
Inventory Product updates remain available if CDMS is down. A later callback
retry or the scheduled query sends the latest Product snapshot again. CDMS
compares snapshots and only writes when data differs.

Database writes are wrapped in transactions. CDMS locks an existing managed
Product while comparing/updating it. The unique primary key prevents duplicate
ManagedProduct rows for concurrent requests.

## Tests

```bash
python manage.py test
```

## Libraries

- Django and Django REST Framework: web framework and REST API.
- psycopg: PostgreSQL driver.
- requests: Inventory callback and scheduled HTTP query.
- openpyxl: `.xlsx` parsing.
- Faker: demo and spike-test seed data.
