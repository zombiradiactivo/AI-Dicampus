// JavaScript legacy con callbacks (Pyramid of Doom)
function getUserData(userId, callback) {
    db.query('SELECT * FROM users WHERE id = ?', [userId], function(err, user) {
        if (err) { callback(err, null); return; }
        db.query('SELECT * FROM orders WHERE user_id = ?', [user.id], function(err, orders) {
            if (err) { callback(err, null); return; }
            orders.forEach(function(order) {
                db.query('SELECT * FROM items WHERE order_id = ?', [order.id], function(err, items) {
                    if (err) { callback(err, null); return; }
                    order.items = items;
                });
            });
            user.orders = orders;
            callback(null, user);
        });
    });
}