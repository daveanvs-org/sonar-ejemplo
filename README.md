# sonar-ejemplo

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sonar-ejemplo&metric=alert_status&token=75cd4c52cfa0bd09175ba751111f3d5a15d5ec4b)](https://sonarcloud.io/summary/new_code?id=sonar-ejemplo)

Proyecto de ejemplo con **FastAPI** para demostrar el análisis de calidad de código con [SonarCloud](https://sonarcloud.io/project/overview?id=sonar-ejemplo).

---

## Ejemplos de issues detectados por SonarCloud

Los siguientes problemas están en [`app/utils.py`](app/utils.py) de forma **intencional** como material didáctico.

### 🔴 Security — SQL Injection (S3649)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-3649)

La query se construye concatenando directamente el input del usuario. Un atacante puede inyectar SQL malicioso y leer, modificar o borrar cualquier dato de la base de datos. Aparece en SonarCloud como **Vulnerability**.

```python
query = "SELECT * FROM items WHERE name = '" + name + "'"  # ← SQL injection
```

### 🔴 Security — Algoritmo de hash débil MD5 (S4790)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-4790)

`hashlib.md5()` está criptográficamente roto y no debe usarse para datos sensibles ni verificación de integridad. Aparece en SonarCloud como **Security Hotspot**.

```python
return hashlib.md5(name.encode()).hexdigest()  # ← weak hash
```

### 🟠 Reliability — Argumento mutable por defecto (S5717)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-5717)

La lista `tags=[]` se comparte entre **todas** las llamadas a la función. Si una llamada la modifica, la siguiente recibe la lista ya modificada, produciendo comportamiento inesperado difícil de depurar. Aparece en SonarCloud como **Bug**.

```python
def build_item_tags(item_name: str, tags: list = []) -> list:  # ← mutable default
    tags.append(item_name)
    return tags
```

### 🟡 Maintainability — Complejidad cognitiva excesiva (S3776)
[Ver regla en SonarCloud](https://rules.sonarsource.com/python/RSPEC-3776)

La función `calculate_final_price` aplica un descuento simple pero con un anidamiento de `if/for` innecesario que dispara la complejidad cognitiva muy por encima del umbral de 15. Aparece en SonarCloud como **Code Smell**.

