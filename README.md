# 🐾 Sistema de Gestión Veterinaria (API REST)

Backend desarrollado con FastAPI para la administración de registros de mascotas y razas. El sistema está completamente dockerizado y listo para su uso.

---

## 📱 Proyecto Móvil
Este backend sirve como motor de datos para la siguiente aplicación:
👉 Repositorio Android App: [Enlace](https://github.com/cristianS97/MascotasAndroid)

---

## 📂 Estructura del Proyecto

```
.
├── routers/               # Lógica de endpoints modularizada
│   ├── mascota.py         # Endpoints de registros de mascotas
│   └── raza.py            # Endpoints de catálogo de razas
├── data/                  # Persistencia de Docker (Postgres y pgAdmin)
├── main.py                # Punto de entrada y configuración de la API
├── models.py              # Modelos de tablas SQLAlchemy
├── database.py            # Gestión de conexión y sesiones de DB
├── Dockerfile             # Configuración de imagen Docker para la API
├── docker-compose.yml     # Orquestación de todos los servicios
└── requirements.txt       # Dependencias del proyecto (incluye psycopg2, sqlalchemy, etc.)
```

---

## 🏗️ Infraestructura y Red
El sistema utiliza Docker Compose con una red interna privada. La API incluye un mecanismo de Healthcheck para asegurar que PostgreSQL esté listo antes de aceptar conexiones.

* API: http://localhost:8000
* pgAdmin: http://localhost:8080 (Admin: admin@admin.com / admin)
* Postgres: Puerto local 5433 mapeado al 5432 interno.

---

## 🚀 Instalación y Ejecución

1. Levantar todo el ecosistema:
   docker-compose up -d --build

2. Documentación Interactiva:
   Accede a Swagger UI en: http://localhost:8000/docs

---

## 🛣️ Catálogo de Endpoints

### 🐕 Gestión de Mascotas (/mascota)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| ![GET](https://img.shields.io/badge/GET-green) | /mascota/ | Lista todas las mascotas (incluye relación con raza). |
| ![GET](https://img.shields.io/badge/GET-green) | /mascota/{id}/ | Detalle individual por ID. |
| ![POST](https://img.shields.io/badge/POST-blue) | /mascota/ | Registro (Valida que el raza_id exista). |
| ![PUT](https://img.shields.io/badge/PUT-orange) | /mascota/{id}/ | Actualización completa de datos. |
| ![DELETE](https://img.shields.io/badge/DELETE-red) | /mascota/{id}/ | Eliminación física del registro. |

### 🐈 Gestión de Razas (/raza)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| ![GET](https://img.shields.io/badge/GET-green) | /raza/ | Lista todas las razas registradas. |
| ![GET](https://img.shields.io/badge/GET-green) | /raza/{id}/ | Detalle de raza por ID. |
| ![GET](https://img.shields.io/badge/GET-green) | /raza/especies/ | Obtiene lista de especies únicas registradas. |
| ![GET](https://img.shields.io/badge/GET-green) | /raza/especie/{especie}/ | Filtra razas por nombre de especie (Perro, Gato, etc.). |
| ![POST](https://img.shields.io/badge/POST-blue) | /raza/ | Registra nueva raza (Evita duplicados nombre/especie). |
| ![PUT](https://img.shields.io/badge/PUT-orange) | /raza/{id}/ | Modifica datos de una raza existente. |
| ![DELETE](https://img.shields.io/badge/DELETE-red) | /raza/{id}/ | Eliminación (Bloqueada si hay mascotas asociadas). |

---

## 🛠️ Tecnologías Principales
* FastAPI: Framework de alto rendimiento.
* SQLAlchemy 2.0: Manejo de relaciones 1:N y consultas complejas.
* Pydantic: Validación estricta de Schemas e integridad de datos.
* Docker: Contenedores para base de datos, API y gestor web.

---

## 💻 Notas para el Desarrollador Android
Para conectar el emulador a la API en Docker, usa la dirección:
http://10.0.2.2:8000