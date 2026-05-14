import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items as items_module

# Reset del estado en memoria antes de cada test
@pytest.fixture(autouse=True)
def reset_db():
    items_module._db.clear()
    items_module._next_id = 1
    yield


client = TestClient(app)


# ─── Health ───────────────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ─── Items: listado vacío ──────────────────────────────────────────────────────

def test_list_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


# ─── Items: crear ítem ────────────────────────────────────────────────────────

def test_create_item():
    payload = {"name": "Laptop", "description": "Una laptop genial", "price": 999.99}
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99


def test_create_item_without_description():
    payload = {"name": "Mouse", "price": 25.0}
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == ""


# ─── Items: obtener por ID ────────────────────────────────────────────────────

def test_get_item():
    client.post("/items/", json={"name": "Teclado", "price": 50.0})
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Teclado"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item no encontrado"


# ─── Items: listar con datos ──────────────────────────────────────────────────

def test_list_items_with_data():
    client.post("/items/", json={"name": "A", "price": 1.0})
    client.post("/items/", json={"name": "B", "price": 2.0})
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ─── Items: eliminar ──────────────────────────────────────────────────────────

def test_delete_item():
    client.post("/items/", json={"name": "Borrar esto", "price": 9.0})
    response = client.delete("/items/1")
    assert response.status_code == 204

    response = client.get("/items/1")
    assert response.status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item no encontrado"
