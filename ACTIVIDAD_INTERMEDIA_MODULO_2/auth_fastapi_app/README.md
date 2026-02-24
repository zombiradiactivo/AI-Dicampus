# 🔐 FastAPI Basic Auth System

Sistema de autenticación modular construido con **FastAPI**, **SQLAlchemy** y **JWT (JSON Web Tokens)**. Este proyecto implementa las mejores prácticas de seguridad, incluyendo hashing de contraseñas con Bcrypt y validación de datos con Pydantic.

## 🚀 Características

* **Registro de Usuarios**: Validación de email único y hashing de contraseñas.
* **Login OAuth2**: Emisión de tokens JWT seguros.
* **Rutas Protegidas**: Middleware para verificar la identidad del usuario.
* **Arquitectura Modular**: Separación clara entre modelos, esquemas, servicios y rutas.
* **Configuración por Entorno**: Manejo de secretos mediante archivos `.env`.

## 🛠️ Tecnologías utilizadas

* [FastAPI](https://fastapi.tiangolo.com/): Framework web moderno y rápido.
* [SQLAlchemy](https://www.sqlalchemy.org/): ORM para la gestión de base de datos.
* [Pydantic](https://docs.pydantic.dev/): Validación de datos y configuraciones.
* [Passlib & Bcrypt](https://passlib.readthedocs.io/): Seguridad y hashing de credenciales.
* [Python-Jose](https://python-jose.readthedocs.io/): Generación y verificación de tokens JWT.

## 📁 Estructura del Proyecto



```text
auth-fastapi-app/
├── app/
│   ├── api/            # Endpoints (auth, users)
│   ├── core/           # Seguridad (JWT) y Configuración
│   ├── crud/           # Lógica de base de datos
│   ├── models/         # Modelos de SQLAlchemy
│   ├── schemas/        # Modelos de Pydantic
│   ├── database.py     # Conexión a DB
│   └── main.py         # Punto de entrada
├── .env                # Variables de entorno
└── requirements.txt    # Dependencias
```

## ⚙️ Instalación y Configuración

Clonar el repositorio:
```Bash
git clone https://github.com/zombiradiactivo/AI-Dicampus
cd AI-Dicampus\ACTIVIDAD_INTERMEDIA_MODULO_2\auth_fastapi_app
```

Instalar dependencias:

```Bash
pip install -r requirements.txt
```

Configurar variables de entorno:
Crea un archivo .env en la raíz con el siguiente contenido:
Fragmento de código

```
SECRET_KEY=tu_clave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./sql_app.db
```
## 🚀 Ejecución

Inicia el servidor de desarrollo con Uvicorn:
```Bash
uvicorn app.main:app --reload
```
El servidor estará disponible en `http://127.0.0.1:8000`.
## 📖 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva:

 -   Swagger UI: http://127.0.0.1:8000/docs

-    ReDoc: http://127.0.0.1:8000/redoc

## 🔒 Flujo de Autenticación

####    POST `/auth/register`: El usuario envía su email y password. La contraseña se hashea y se guarda.

####    POST `/auth/login`: El usuario envía credenciales. Si son válidas, recibe un access_token.

####    GET `/auth/me`: El cliente envía el token en el header Authorization: Bearer <token> para obtener su perfil.

## ⚠️ Notas de Seguridad

    La versión de bcrypt debe ser 4.0.1 para mantener compatibilidad con passlib.