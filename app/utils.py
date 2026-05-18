import hashlib

# ──────────────────────────────────────────────────────────────────────────────
# SECURITY — S4790: Use of weak hashing algorithm (MD5)
# SonarCloud lo reporta como Security Hotspot / Vulnerability
# MD5 es criptográficamente débil y no debe usarse para datos sensibles
# ──────────────────────────────────────────────────────────────────────────────
def hash_item_name(name: str) -> str:
    return hashlib.md5(name.encode()).hexdigest()  # noqa: S324


# ──────────────────────────────────────────────────────────────────────────────
# RELIABILITY — S5717: Mutable default argument (Bug)
# SonarCloud lo reporta como Bug
# La lista `tags=[]` se comparte entre todas las llamadas a la función
# lo que produce comportamiento inesperado en llamadas sucesivas
# ──────────────────────────────────────────────────────────────────────────────
def build_item_tags(item_name: str, tags: list = []) -> list:  # noqa: B006
    tags.append(item_name)
    return tags


# ──────────────────────────────────────────────────────────────────────────────
# MAINTAINABILITY — S1481: Variable local sin usar (Code Smell)
# SonarCloud lo reporta como Code Smell
# `temp` se asigna pero nunca se utiliza
# ──────────────────────────────────────────────────────────────────────────────
def calculate_final_price(price: float, discount: float) -> float:
    temp = price * 100  # variable asignada y nunca usada
    if discount > 0:
        return price - (price * discount / 100)
    return price
