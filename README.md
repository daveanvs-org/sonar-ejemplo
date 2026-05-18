# sonar-ejemplo

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sonar-ejemplo&metric=alert_status&token=75cd4c52cfa0bd09175ba751111f3d5a15d5ec4b)](https://sonarcloud.io/summary/new_code?id=sonar-ejemplo)

Proyecto de ejemplo con **FastAPI** para demostrar el análisis de calidad de código con [SonarCloud](https://sonarcloud.io/project/overview?id=sonar-ejemplo).

---

## Ejemplos de issues detectados por SonarCloud

Los siguientes problemas están en [`app/utils.py`](app/utils.py) de forma **intencional** como material didáctico.

### 🔴 Security — Credencial hardcodeada (S6437)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-6437)

Un `API_SECRET_TOKEN` escrito directamente en el código queda expuesto en el historial de Git. Cualquier persona con acceso al repositorio puede extraerlo.

```python
API_SECRET_TOKEN = "sk-prod-4aB9xQ2rTz8mKvLp1NcW"  # ← hardcoded credential
```

### 🔴 Security — Algoritmo de hash débil MD5 (S4790)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-4790)

`hashlib.md5()` está criptográficamente roto y no debe usarse para datos sensibles ni verificación de integridad.

```python
return hashlib.md5(name.encode()).hexdigest()  # ← weak hash
```

### 🟠 Reliability — Recurso abierto que nunca se cierra (S2674)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-2674)

`open()` sin `with` ni `close()` deja el descriptor de archivo abierto si ocurre una excepción, agotando los recursos del sistema operativo.

```python
f = open(filepath)   # ← nunca se llama f.close()
reader = csv.reader(f)
```

### 🟡 Maintainability — Complejidad cognitiva excesiva (S3776)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-3776)

La función `calculate_final_price` aplica un descuento simple pero con un anidamiento de `if/for` innecesario que dispara la complejidad cognitiva muy por encima del umbral de 15. Debería reescribirse en 3 líneas.
