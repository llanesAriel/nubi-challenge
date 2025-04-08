# nubi-challenge
Solución al coding challenge de Nubi: desarrollo de una API REST en Python utilizando FastAPI. Incluye endpoints para la gestión de usuarios, protección de endpoints, paginación, ordenamiento, filtrado, tests unitarios y despliegue con Docker.

Incluye:
- Aplicación FastAPI
- Tests
- Seguridad con API Key
- Dockerfile para contenerizar la aplicación

## ¿Cómo ejecutar el proyecto?

### 1. Levantar la API localmente usando Docker Compose

```bash
docker-compose up --build
```

Esto construirá la imagen y levantará la API en:

```
http://localhost:8000
```

### 2. Ejecutar los tests unitarios

```bash
docker compose --profile test run --rm test
```

Esto construirá la imagen si es necesario y ejecutará los tests con Pytest dentro del contenedor.

## Pre-commit hooks

Este proyecto utiliza **pre-commit** para asegurar la calidad del código automáticamente antes de cada commit.

Se utilizan los siguientes hooks:
- `ruff`: Linting y ordenamiento de imports.
- `ruff-format`: Formateo automático de código.

### ¿Cómo instalar pre-commit?

**Nota:** Pre-commit es una herramienta de desarrollo, no está incluida en `requirements.txt`.

La mejor práctica es instalar herramientas de desarrollo usando `pipx`, para mantenerlas aisladas del entorno del proyecto.

1. Asegurate de tener `pipx` instalado:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath