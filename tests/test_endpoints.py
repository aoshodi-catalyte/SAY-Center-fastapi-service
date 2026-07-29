"""
Integration tests for product_service API endpoints using REAL Postgres.
"""

import pytest
from fastapi.testclient import TestClient

from database import Base, engine, SessionLocal
from product_service import app, get_db


@pytest.fixture
def client():
    """
    Provide a TestClient backed by the real Postgres database.
    Each test starts with a clean schema.
    """

    # Reset schema on Postgres
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Real DB session per request
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def _valid_product_payload(**overrides) -> dict:
    payload = {
        "name": "Basil Plant - 4in Pot",
        "unit": "kg",
        "cost_per_unit": 1.75,
        "price_per_unit": 4.99,
        "quantity_in_stock": 40,
    }
    payload.update(overrides)
    return payload


def _create_product(client: TestClient, **overrides) -> dict:
    response = client.post("/products", json=_valid_product_payload(**overrides))
    assert response.status_code == 201
    return response.json()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!"}


def test_post_product_creates_and_returns_product(client):
    payload = _valid_product_payload()
    response = client.post("/products", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] is not None
    assert body["name"] == payload["name"]
    assert body["unit"] == payload["unit"]
    assert body["cost_per_unit"] == payload["cost_per_unit"]
    assert body["price_per_unit"] == payload["price_per_unit"]
    assert body["quantity_in_stock"] == payload["quantity_in_stock"]


def test_post_product_rejects_invalid_unit(client):
    response = client.post(
        "/products", json=_valid_product_payload(unit="invalid-unit")
    )
    assert response.status_code == 422


def test_post_product_rejects_empty_name(client):
    response = client.post("/products", json=_valid_product_payload(name="   "))
    assert response.status_code == 422


def test_post_product_rejects_negative_cost(client):
    response = client.post("/products", json=_valid_product_payload(cost_per_unit=-1.0))
    assert response.status_code == 422


def test_post_product_rejects_zero_price(client):
    response = client.post("/products", json=_valid_product_payload(price_per_unit=0))
    assert response.status_code == 422


def test_get_products_returns_empty_list(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_get_products_returns_all_products(client):
    first = _create_product(client, name="Apple Tree")
    second = _create_product(client, name="Banana Tree")

    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 2
    assert {p["id"] for p in products} == {first["id"], second["id"]}


def test_search_products_by_name(client):
    _create_product(client, name="Shared Name", unit="kg")
    _create_product(client, name="Other Product", unit="lb")

    response = client.get("/products/search", params={"name": "Shared Name"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Shared Name"


def test_search_products_by_name_and_unit(client):
    _create_product(client, name="Shared Name", unit="kg")
    _create_product(client, name="Shared Name", unit="lb")

    response = client.get(
        "/products/search", params={"name": "Shared Name", "unit": "lb"}
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["unit"] == "lb"


def test_search_products_returns_empty_when_no_match(client):
    _create_product(client, name="Apple Tree")

    response = client.get("/products/search", params={"name": "Missing Product"})
    assert response.status_code == 200
    assert response.json() == []


def test_db_check_reports_connected_and_product_count(client):
    _create_product(client)
    _create_product(client, name="Second Product")

    response = client.get("/db-check")
    assert response.status_code == 200
    assert response.json() == {"status": "connected", "product_count": 2}


def test_db_check_returns_500_when_query_fails(client):
    class BrokenSession:
        def query(self, *args, **kwargs):
            raise Exception("db down")

        def close(self):
            pass

    def broken_get_db():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_get_db

    response = client.get("/db-check")
    assert response.status_code == 500
    assert "Database connection failed" in response.json()["detail"]


def test_get_product_by_id_returns_product(client):
    created = _create_product(client)

    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_product_by_id_returns_404_when_missing(client):
    response = client.get("/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product does not exist."}


def test_delete_product_removes_product(client):
    created = _create_product(client)

    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/products/{created['id']}")
    assert get_response.status_code == 404


def test_delete_product_returns_404_when_missing(client):
    response = client.delete("/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product does not exist"}


def test_update_product_replaces_fields(client):
    created = _create_product(client)
    updated_payload = _valid_product_payload(
        name="Updated Basil Plant",
        unit="each",
        cost_per_unit=2.0,
        price_per_unit=5.99,
        quantity_in_stock=25,
    )

    response = client.put(f"/products/{created['id']}", json=updated_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["name"] == updated_payload["name"]
    assert body["unit"] == updated_payload["unit"]
    assert body["cost_per_unit"] == updated_payload["cost_per_unit"]
    assert body["price_per_unit"] == updated_payload["price_per_unit"]
    assert body["quantity_in_stock"] == updated_payload["quantity_in_stock"]


def test_update_product_returns_404_when_missing(client):
    response = client.put(
        "/products/9999", json=_valid_product_payload(name="Missing Product")
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product does not exist"}
