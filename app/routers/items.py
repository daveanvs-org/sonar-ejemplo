from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

# Simulamos una "base de datos" en memoria
_db: dict[int, dict] = {}
_next_id = 1


class ItemCreate(BaseModel):
    name: str
    description: str = ""
    price: float


class ItemResponse(ItemCreate):
    id: int


@router.get("/", response_model=list[ItemResponse])
def list_items():
    return [ItemResponse(id=k, **v) for k, v in _db.items()]


@router.get("/{item_id}", response_model=ItemResponse, responses={404: {"description": "Item no encontrado"}})
def get_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return ItemResponse(id=item_id, **_db[item_id])


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    global _next_id
    _db[_next_id] = item.model_dump()
    created = ItemResponse(id=_next_id, **_db[_next_id])
    _next_id += 1
    return created


@router.delete("/{item_id}", status_code=204, responses={404: {"description": "Item no encontrado"}})
def delete_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del _db[item_id]


# =============================================================================
# SECURITY — python:S3649: SQL Injection (Vulnerability)
# Regla: https://rules.sonarsource.com/python/RSPEC-3649
# El parámetro `name` viene directamente del query string del usuario HTTP.
# Se concatena sin sanitizar en la query SQL, permitiendo a un atacante
# inyectar SQL arbitrario.  Ejemplo: name = "' OR '1'='1"
# Aparece en SonarCloud como Vulnerability en Security.
# =============================================================================
@router.get("/search")
def search_items(name: str):
    query = "SELECT * FROM items WHERE name = '" + name + "'"  # ← SQL injection
    return {"query": query}

