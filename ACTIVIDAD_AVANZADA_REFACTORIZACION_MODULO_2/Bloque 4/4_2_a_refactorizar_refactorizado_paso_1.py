def process_orders(orders: list, discounts: dict, inventory_list: list):
    # --- OPTIMIZACIÓN O(n^2) -> O(n) ---
    # Transformamos la lista en un diccionario indexado por ID
    # Esto permite búsquedas instantáneas en lugar de recorrer toda la lista
    inventory_map = {item['id']: item for item in inventory_list}
    
    results = []
    for order in orders:
        total = 0
        for item in order['items']:
            # Búsqueda O(1) en el mapa de inventario
            product = inventory_map.get(item['id'])
            
            if product:
                if product['stock'] > 0:
                    total += item['qty'] * product['price']
            else:
                # Mantenemos el log de error original por ahora
                print(f"Item not found: {item['id']}")
        
        # El resto de la lógica de descuentos se mantiene igual 
        # (se refactorizará en los siguientes pasos)
        if order['type'] == 'premium':
            total = total * (1 - discounts['premium'])
        elif order['type'] == 'vip':
            total = total * (1 - discounts['vip'])
            if total > 1000:
                total = total * 0.95
        elif order['type'] == 'bulk':
            if len(order['items']) > 10:
                total = total * (1 - discounts['bulk'])
        
        results.append({'order_id': order['id'], 'total': round(total, 2)})
        
    return results