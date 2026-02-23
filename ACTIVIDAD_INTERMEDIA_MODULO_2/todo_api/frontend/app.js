const API_URL = "http://127.0.0.1:8000/tasks";

// 1. Función para obtener y mostrar tareas (GET)
async function fetchTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();
    
    const list = document.getElementById('taskList');
    list.innerHTML = ''; // Limpiar lista actual

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = task.completed ? 'completed' : '';
        
        li.innerHTML = `
            <span onclick="toggleTask(${task.id}, ${task.completed}, '${task.title}')" style="cursor:pointer">
                ${task.completed ? '✅' : '⬜'} ${task.title}
            </span>
            <button class="delete-btn" onclick="deleteTask(${task.id})">Eliminar</button>
        `;
        list.appendChild(li);
    });
}

// 2. Función para crear tarea (POST)
async function createTask() {
    const input = document.getElementById('taskInput');
    const title = input.value;

    if (!title) return alert("Escribe algo!");

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title, description: "Creada desde el frontend" })
    });

    input.value = '';
    fetchTasks(); // Recargar la lista
}

// 3. Función para eliminar tarea (DELETE)
async function deleteTask(taskId) {
    if(!confirm("¿Seguro que quieres borrarla?")) return;

    await fetch(`${API_URL}/${taskId}`, {
        method: 'DELETE'
    });
    fetchTasks();
}

// 4. Función para actualizar estado (PUT)
// Nota: Enviamos el título de nuevo porque nuestro PUT original requiere el objeto completo
async function toggleTask(id, currentStatus, currentTitle) {
    await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            title: currentTitle, 
            completed: !currentStatus 
        })
    });
    fetchTasks();
}

// Cargar tareas al iniciar
fetchTasks();