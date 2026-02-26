import sqlite3
import os

DB_FILE = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Para poder acceder por nombre de columna
    return conn

# Inicialización de tablas
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Tabla de Tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT 'todo',
            due_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabla de Auditoría
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT,
            action TEXT,
            details TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Ejecutar inicialización al importar
init_db()

# Función para guardar logs (la usará tu sistema de auditoría)
def save_audit_log(user_id: str, action: str, details: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
        (user_id, action, details)
    )
    conn.commit()
    conn.close()

# LA FUNCIÓN QUE FALTA:
def get_all_audit_logs():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- FUNCIONES DE USUARIO ---
def save_user(user_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (user_data['username'], user_data['password_hash'], user_data.get('role', 'user'))
        )
        conn.commit()
        user_data['id'] = cursor.lastrowid
        return user_data
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(user) if user else None

# --- FUNCIONES DE TAREAS ---
def save_task(task_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, title, description, priority, due_date) VALUES (?, ?, ?, ?, ?)",
        (task_data['user_id'], task_data['title'], task_data.get('description', ''), 
         task_data.get('priority', 1), task_data.get('due_date', ''))
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    task_data['id'] = task_id
    return task_data

def fetch_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    # Obtenemos todas las tareas sin filtrar por ID
    rows = cursor.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_tasks_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True

# Función para editar (Extra para que la tengas)
def update_task_title(task_id: int, new_title: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    conn.commit()
    conn.close()