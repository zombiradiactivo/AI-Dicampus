const express = require('express');
const jwt = require('jsonwebtoken');
const app = express();

app.use(express.json()); // Middleware para entender body en formato JSON

// Clave secreta para firmar el token (En producción usa variables de entorno)
const SECRET_KEY = "mi_clave_super_secreta_123";

/**
 * POST /login
 * @body {string} username - Nombre de usuario
 * @body {string} password - Contraseña
 */
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    // 1. Simulación de validación (Aquí consultarías tu Base de Datos)
    if (username === "admin" && password === "1234") {
        
        // 2. Crear el Payload (datos que viajan en el token)
        const payload = {
            usuario: username,
            rol: "admin"
        };

        // 3. Generar el JWT (Expiración en 1 hora)
        const token = jwt.sign(payload, SECRET_KEY, { expiresIn: '1h' });

        return res.status(200).json({
            mensaje: "Autenticación exitosa",
            token: token
        });
    }

    // 4. Si las credenciales fallan
    return res.status(401).json({
        error: "Usuario o contraseña incorrectos"
    });
});

app.listen(3000, () => console.log("Servidor corriendo en http://localhost:3000"));