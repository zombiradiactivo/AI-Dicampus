
# 📝 To-Do List API con FastAPI y JavaScript

Una aplicación web completa de gestión de tareas (To-Do List). Este proyecto demuestra cómo construir una **API RESTful** robusta utilizando **Python (FastAPI)** para el backend y una interfaz de usuario sencilla utilizando **Vanilla JavaScript (HTML/CSS)**.

![Estado del Proyecto](https://img.shields.io/badge/Estado-Terminado-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)

## 🚀 Características

- **API REST Completa**: Endpoints para crear, leer, actualizar y eliminar tareas (CRUD).
- **Base de Datos Persistente**: Uso de **SQLite** con **SQLAlchemy** (ORM).
- **Validación de Datos**: Esquemas robustos usando **Pydantic**.
- **Documentación Automática**: Swagger UI y ReDoc integrados.
- **Frontend Interactivo**: Interfaz web ligera sin frameworks pesados, conectada vía `fetch`.
- **CORS Configurado**: Comunicación segura entre frontend y backend.

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y de alto rendimiento.
- **Uvicorn**: Servidor ASGI.
- **SQLAlchemy**: Toolkit SQL y ORM.
- **Pydantic**: Validación de datos.
- **Python-dotenv**: Gestión de variables de entorno.

### Frontend
- **HTML5 / CSS3**: Estructura y estilos.
- **JavaScript (ES6+)**: Lógica del cliente y consumo de API.

---

## 📂 Estructura del Proyecto

```text
todo_api/
├── .env                  # Variables de entorno (URL base de datos)
├── .gitignore            # Archivos ignorados por Git
├── requirements.txt      # Dependencias de Python
├── tasks.db              # Archivo de Base de Datos (se genera automáticamente)
│
├── app/                  # Lógica del Backend
│   ├── __init__.py
│   ├── main.py           # Punto de entrada y configuración de CORS
│   ├── database.py       # Conexión a SQLite
│   ├── models.py         # Modelos de Base de Datos (SQLAlchemy)
│   ├── schemas.py        # Esquemas de Validación (Pydantic)
│   └── routers/
│       ├── __init__.py
│       └── tasks.py      # Endpoints (GET, POST, PUT, DELETE)
│
└── frontend/             # Interfaz de Usuario
    ├── index.html
    ├── styles.css
    └── app.js
```

---

## ⚡ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu máquina local.


### 1. Configurar el entorno virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto y añade:
```properties
DATABASE_URL=sqlite:///./tasks.db
```

---

## ▶️ Ejecución

Necesitarás dos terminales abiertas: una para el Backend y otra para servir el Frontend (opcional, pero recomendado).

### Terminal 1: Backend (API)
Inicia el servidor de FastAPI:
```bash
uvicorn app.main:app --reload
```
*La API estará corriendo en: `http://127.0.0.1:8000`*

### Terminal 2: Frontend
Para evitar problemas de CORS con los navegadores modernos, sirve los archivos estáticos:
```bash
cd frontend
python -m http.server 3000
```
*La web estará disponible en: `http://127.0.0.1:3000`*

---

## 📖 Documentación de la API

FastAPI genera documentación interactiva automáticamente. Una vez encendido el backend, visita:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Para probar los endpoints directamente.
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Documentación alternativa.

### Endpoints Principales

| Método | Endpoint         | Descripción                          |
|--------|------------------|--------------------------------------|
| `GET`  | `/tasks/`        | Obtener todas las tareas             |
| `POST` | `/tasks/`        | Crear una nueva tarea                |
| `PUT`  | `/tasks/{id}`    | Actualizar una tarea existente       |
| `DELETE`| `/tasks/{id}`   | Eliminar una tarea                   |

---


## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.