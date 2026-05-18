import csv
import hashlib

# =============================================================================
# SECURITY #1 — python:S6437: Credencial hardcodeada
# Regla: https://rules.sonarsource.com/python/RSPEC-6437
# Un token/contraseña escrito directamente en el código queda expuesto
# en el historial de Git y puede ser extraído por cualquiera con acceso
# al repositorio.
# =============================================================================
API_SECRET_TOKEN = "sk-prod-4aB9xQ2rTz8mKvLp1NcW"   # noqa: S105  ← hardcoded credential


def get_auth_header() -> dict:
    return {"Authorization": f"Bearer {API_SECRET_TOKEN}"}


# =============================================================================
# SECURITY #2 — python:S4790: Algoritmo de hash débil (MD5)
# Regla: https://rules.sonarsource.com/python/RSPEC-4790
# MD5 está criptográficamente roto; no debe usarse para datos sensibles
# ni como función de verificación de integridad en contextos de seguridad.
# =============================================================================
def hash_item_name(name: str) -> str:
    return hashlib.md5(name.encode()).hexdigest()  # noqa: S324  ← weak hash


# =============================================================================
# RELIABILITY — python:S2674: Recurso abierto que nunca se cierra (Resource Leak)
# Regla: https://rules.sonarsource.com/python/RSPEC-2674
# El archivo CSV se abre con open() pero si ocurre una excepción antes de
# llegar al final de la función el archivo queda abierto indefinidamente,
# consumiendo descriptores de archivo del sistema operativo.
# =============================================================================
def read_item_prices(filepath: str) -> list[float]:
    f = open(filepath)          # ← archivo nunca cerrado con close() ni with
    reader = csv.reader(f)
    prices = []
    for row in reader:
        if row:
            prices.append(float(row[0]))
    return prices


# =============================================================================
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
