import hashlib

# =============================================================================
# SECURITY #1 — python:S6437: Contraseña hardcodeada (Security Hotspot)
# Las credenciales de base de datos escritas directamente en el código quedan
# expuestas en el historial de Git. Cualquier persona con acceso al repositorio
# puede extraerlas y conectarse a la base de datos directamente.
# Aparece en SonarCloud como Security Hotspot.
# =============================================================================
DB_HOST = "prod-db.empresa.com"
DB_USER = "admin"
DB_PASSWORD = "P@ssw0rd_Prod_2024!"  # noqa: S105  ← hardcoded password


def get_db_connection():
    return f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/items_db"


# =============================================================================
# SECURITY #2 — python:S4790: Algoritmo de hash débil (MD5)
# MD5 está criptográficamente roto; no debe usarse para datos sensibles.
# Aparece en SonarCloud como Security Hotspot (requiere revisión humana).
# =============================================================================
def hash_item_name(name: str) -> str:
    return hashlib.md5(name.encode()).hexdigest()  # noqa: S324  ← weak hash


# =============================================================================
# RELIABILITY — python:S1763: Código inalcanzable después de un return (Bug)
# Regla: https://rules.sonarsource.com/python/RSPEC-1763
# Las líneas después del return nunca se ejecutarán. Suele indicar una
# refactorización incompleta o un error lógico del desarrollador.
# Aparece en SonarCloud como Bug en Reliability.
# =============================================================================
def get_item_status(price: float) -> str:
    if price > 100:
        return "expensive"
    return "cheap"
    print(f"Price checked: {price}")  # noqa: T201  ← unreachable code after return


# =============================================================================
# MAINTAINABILITY — python:S3776: Complejidad cognitiva demasiado alta
# Regla: https://rules.sonarsource.com/python/RSPEC-3776
# Esta función aplica un descuento simple pero lo implementa con anidamiento
# excesivo de condiciones y bucles que disparan la complejidad cognitiva
# muy por encima del umbral recomendado (15). Debería reescribirse en 3 líneas.
# Aparece en SonarCloud como Code Smell en Maintainability.
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


# =============================================================================
# DUPLICACIÓN — Copia exacta de calculate_final_price para disparar el
# detector de código duplicado (CPD) de SonarCloud y subir el % de Duplications
# =============================================================================
def compute_final_price(price: float, discount: float, currency: str = "MXN") -> float:
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

