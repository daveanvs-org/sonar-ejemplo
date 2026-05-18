# sonar-ejemplo

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sonar-ejemplo&metric=alert_status&token=75cd4c52cfa0bd09175ba751111f3d5a15d5ec4b)](https://sonarcloud.io/summary/new_code?id=sonar-ejemplo)

Proyecto de ejemplo con **FastAPI** para demostrar el análisis de calidad de código con [SonarCloud](https://sonarcloud.io/project/overview?id=sonar-ejemplo).

---

## Ejemplos de issues detectados por SonarCloud

Los ejemplos están en [`app/utils.py`](app/utils.py) y [`app/routers/items.py`](app/routers/items.py) de forma **intencional** como material didáctico.

> **Nota sobre el Quality Gate:** Tener issues no significa automáticamente reprobar la métrica. SonarCloud evalúa un *rating* (A–E). Para que una métrica repruebe, el rating debe ser peor que A en código nuevo: basta **1 Bug** para que Reliability sea E, **1 Vulnerability** para que Security sea E. Maintainability evalúa el ratio de deuda técnica (deuda en minutos / costo estimado de desarrollo), por lo que en proyectos pequeños se mantiene en A aunque haya Code Smells.

---

### 🔴 Security — SQL Injection (S3649) — `app/routers/items.py`
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-3649)

El query parameter `name` viene directamente del usuario HTTP y se concatena sin sanitizar en una query SQL. Sonar lo detecta mediante *taint analysis* (rastrea el flujo del dato desde el input HTTP hasta la query). Aparece como **Vulnerability** en Security.

```python
@router.get("/search")
def search_items(name: str):
    query = "SELECT * FROM items WHERE name = '" + name + "'"  # ← SQL injection
```

### 🔴 Security — Hash débil MD5 (S4790) — `app/utils.py`
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-4790)

MD5 está criptográficamente roto. Sonar no puede determinar si es un uso sensible sin contexto humano, por eso aparece como **Security Hotspot** (no Vulnerability) — requiere revisión manual.

```python
return hashlib.md5(name.encode()).hexdigest()  # ← weak hash
```

---

### 🟠 Reliability — Código inalcanzable tras return (S1763) — `app/utils.py`
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-1763)

El `print` después del `return` nunca se ejecutará. Suele indicar una refactorización incompleta. Aparece como **Bug** en Reliability.

```python
def get_item_status(price: float) -> str:
    if price > 100:
        return "expensive"
    return "cheap"
    print(f"Price checked: {price}")  # ← unreachable code after return
```

---

### 🟡 Maintainability — Complejidad cognitiva excesiva (S3776) — `app/utils.py`
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-3776)

`calculate_final_price` aplica un descuento simple con anidamiento `if/for` innecesario (complejidad cognitiva 62, umbral = 15). Aparece como **Code Smell** en Maintainability. La función podría reescribirse en 3 líneas.


