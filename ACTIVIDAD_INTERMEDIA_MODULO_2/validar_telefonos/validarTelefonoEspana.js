/**
 * Valida si un número de teléfono sigue el formato internacional español (+34XXXXXXXXX).
 * * @param {string} telefono - El número de teléfono a validar.
 * @returns {boolean} - Retorna true si es válido, false de lo contrario.
 */
function validarTelefonoEspana(telefono) {
    // Explicación del patrón:
    // ^        : Inicio de la cadena.
    // \+34     : El prefijo literal +34.
    // [6789]   : El primer dígito tras el prefijo (6, 7 para móvil; 8, 9 para fijo).
    // \d{8}    : Exactamente 8 dígitos numéricos adicionales.
    // $        : Fin de la cadena.
    const patron = /^\+34[6789]\d{8}$/;

    return patron.test(telefono);
}

// --- Casos de Prueba ---
const pruebas = [
    { num: "+34611222333", esperado: true },  // Móvil válido
    { num: "+34932112233", esperado: true },  // Fijo válido
    { num: "611222333",    esperado: false }, // Falta +34
    { num: "+34511222333", esperado: false }, // Empieza por 5 (no válido)
    { num: "+346112223334", esperado: false } // Demasiados dígitos
];

console.table(pruebas.map(p => ({
    Número: p.num,
    Resultado: validarTelefonoEspana(p.num) ? "✅ Válido" : "❌ Inválido",
    Correcto: validarTelefonoEspana(p.num) === p.esperado ? "👍" : "👎"
})));