import hashlib

# =============================================================================
# SECURITY — python:S3649: SQL Injection (Vulnerability)
# Regla: https://rules.sonarsource.com/python/RSPEC-3649
# La query se construye concatenando directamente el input del usuario.
# Un atacante puede inyectar SQL malicioso y leer, modificar o borrar
# cualquier dato de la base de datos.
#   Ejemplo de ataque: name = "' OR '1'='1"
# =============================================================================
def search_items_by_name(db_conn, name: str):
    query = "SELECT * FROM items WHERE name = '" + name + "'"  # ← SQL injection
    return db_conn.execute(query)


# =============================================================================
# SECURITY #2 — python:S4790: Algoritmo de hash débil (MD5)
# Regla: https://rules.sonarsource.com/python/RSPEC-4790
# MD5 está criptográficamente roto; no debe usarse para datos sensibles.
# (Este aparece en Security Hotspots en SonarCloud)
# =============================================================================
def hash_item_name(name: str) -> str:
    return hashlib.md5(name.encode()).hexdigest()  # noqa: S324  ← weak hash


# =============================================================================
# RELIABILITY — python:S5717: Argumento mutable por defecto (Bug)
# Regla: https://rules.sonarsource.com/python/RSPEC-5717
# La lista `tags=[]` se comparte entre TODAS las llamadas a la función.
# Si una llamada la modifica, la siguiente llamada recibe la lista ya modificada,
# produciendo comportamiento inesperado difícil de depurar.
# =============================================================================
def build_item_tags(item_name: str, tags: list = []) -> list:  # noqa: B006  ← mutable default
    tags.append(item_name)
    return tags


# MAINTAINABILITY — python:S3776: Complejidad cognitiva demasiado alta
# Regla: https://rules.sonarsource.com/python/RSPEC-3776
# Esta función aplica un descuento simple pero lo implementa con anidamiento
# excesivo de condiciones y bucles que disparan la complejidad cognitiva
# muy por encima del umbral recomendado (15). Debería reescribirse en 3 líneas.
# =============================================================================
def calculate_final_price(price: float, discount: float, currency: str = "MXN") -> float:
    result = price
    if price > 0:
        if discount > 0:
            if discount < 100:
                if currency == "MXN":
                    for _ in range(1):
                        if discount >= 50:
                            if price > 1000:
                                result = (price - (price * discount / 100)) * 0.84
                            else:
                                result = price - (price * discount / 100)
                        else:
                            if price > 500:
                                result = (price - (price * discount / 100)) * 1.16
                            else:
                                result = price - (price * (discount * 0.9) / 100)
                elif currency == "USD":
                    for _ in range(1):
                        if discount >= 50:
                            result = (price - (price * discount / 100)) * 17.15
                        else:
                            result = (price - (price * discount / 100)) * 17.50
                elif currency == "EUR":
                    if discount >= 30:
                        result = (price - (price * discount / 100)) * 18.20
                    else:
                        result = (price - (price * discount / 100)) * 18.60
                else:
                    result = price - (price * discount / 100)
            else:
                result = 0.0
        else:
            result = price
    else:
        result = 0.0
    return result
