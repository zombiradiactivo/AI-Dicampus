// Refactorizado: Promisified database wrapper
const db = {
    query: (sql, params) => {
        return new Promise((resolve, reject) => {
            db._query(sql, params, (err, result) => {
                if (err) reject(err);
                else resolve(result);
            });
        });
    }
};

/**
 * Obtiene los datos del usuario con sus órdenes e items
 * @param {number} userId - ID del usuario
 * @returns {Promise<Object>} Objeto del usuario con órdenes e items
 * @throws {Error} Si ocurre algún error en las consultas
 */
async function getUserData(userId) {
    try {
        // Obtener usuario
        const [user] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
        
        if (!user) {
            throw new Error(`Usuario con ID ${userId} no encontrado`);
        }

        // Obtener órdenes del usuario
        const orders = await db.query('SELECT * FROM orders WHERE user_id = ?', [user.id]);

        // Obtener items para todas las órdenes en paralelo (CORRECCIÓN DEL BUG)
        const ordersWithItems = await Promise.all(
            orders.map(async (order) => {
                const items = await db.query('SELECT * FROM items WHERE order_id = ?', [order.id]);
                return { ...order, items };
            })
        );

        return {
            ...user,
            orders: ordersWithItems
        };
    } catch (error) {
        console.error('Error obteniendo datos del usuario:', error.message);
        throw error;
    }
}