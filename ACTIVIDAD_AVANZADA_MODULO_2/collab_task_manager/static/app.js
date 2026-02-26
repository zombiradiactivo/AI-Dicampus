const API_URL = "/api";

// Función central para mostrar/ocultar secciones
function showApp(visible) {
    const authElem = document.getElementById('auth-section');
    const appElem = document.getElementById('app-section');

    if (authElem && appElem) {
        if (visible) {
            authElem.style.display = 'none';
            appElem.style.display = 'block';
            loadTasks();
        } else {
            authElem.style.display = 'block';
            appElem.style.display = 'none';
        }
    } else {
        console.error("Error: No se encontraron los contenedores HTML (auth-section o app-section)");
    }
}

async function handleAuth(type) {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    if (!user || !pass) return alert("Completa los campos");

    try {
        const response = await fetch(`${API_URL}/${type}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (response.ok) {
            if (type === 'login') {
                localStorage.setItem('token', data.access_token);
                showApp(true);
            } else {
                alert("Registro exitoso. Ya puedes iniciar sesión.");
            }
        } else {
            alert(data.detail || "Error en la operación");
        }
    } catch (err) {
        console.error("Error en handleAuth:", err);
        alert("Error de conexión con el servidor");
    }
}

async function createNewTask() {
    const title = document.getElementById('task-title').value;
    const desc = document.getElementById('task-desc').value;
    const priority = document.getElementById('task-priority').value;
    const token = localStorage.getItem('token');

    if (!title) return alert("El título es obligatorio");

    try {
        await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                description: desc || "Sin descripción",
                priority: parseInt(priority),
                due_date: new Date().toLocaleDateString()
            })
        });
        document.getElementById('task-title').value = '';
        document.getElementById('task-desc').value = '';
        loadTasks();
    } catch (err) { alert("Error al crear tarea"); }
}

async function editTask(taskId) {
    const newTitle = prompt("Introduce el nuevo título para la tarea:");
    if (!newTitle) return;

    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ title: newTitle })
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (err) {
        alert("Error al actualizar");
    }
}

async function loadTasks() {
    const token = localStorage.getItem('token');
    const list = document.getElementById('task-list');
    const response = await fetch(`${API_URL}/tasks`, { headers: { 'Authorization': `Bearer ${token}` } });
    const result = await response.json();
    
    if (response.ok) {
        list.innerHTML = result.data.map(t => `
            <div class="task-card priority-${t.priority}">
                <div>
                    <strong>${t.title}</strong><br>
                    <small>${t.description}</small>
                </div>
                <button class="delete-btn" onclick="deleteTask(${t.id})">Borrar</button>
            </div>
        `).join('');
    }
}

async function deleteTask(taskId) {
    if (!confirm("¿Seguro que quieres borrar esta tarea?")) return;
    const token = localStorage.getItem('token');
    try {
        await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadTasks();
    } catch (err) { alert("Error al borrar"); }
}

function logout() {
    localStorage.removeItem('token');
    showApp(false);
}

// Al cargar la página, verificamos si ya hay un token
window.onload = () => {
    if (localStorage.getItem('token')) {
        showApp(true);
    }
};