from typing import List, Dict, TypedDict

# Modernización: Definimos estructuras claras para los datos
class OrderItem(TypedDict):
    id: int
    qty: int

class Order(TypedDict):
    id: int
    type: str  # 'premium', 'vip', 'bulk'
    items: List[OrderItem]

class Product(TypedDict):
    id: int
    stock: int
    price: float

def process_orders(
    orders: List[Order], 
    discount_rates: Dict[str, float], 
    inventory_data: List[Product]
) -> List[Dict]:
    
    # Mantenemos la optimización del paso 1 con nombres claros
    inventory_registry = {product['id']: product for product in inventory_data}
    processed_results = []

    for order in orders:
        current_order_total = 0.0
        
        for item in order['items']:
            product = inventory_registry.get(item['id'])
            
            if product:
                if product['stock'] > 0:
                    # Nomenclatura semántica: cantidad * precio
                    line_item_total = item['qty'] * product['price']
                    current_order_total += line_item_total
            else:
                print(f"ALERTA: Producto con ID {item['id']} no encontrado en inventario.")

        # Lógica de descuentos (aún sin Strategy, pero con nombres legibles)
        order_type = order['type']
        
        if order_type == 'premium':
            discount = discount_rates.get('premium', 0)
            current_order_total *= (1 - discount)
            
        elif order_type == 'vip':
            discount = discount_rates.get('vip', 0)
            current_order_total *= (1 - discount)
            # Regla de negocio específica para VIP
            if current_order_total > 1000:
                current_order_total *= 0.95
                
        elif order_type == 'bulk':
            if len(order['items']) > 10:
                discount = discount_rates.get('bulk', 0)
                current_order_total *= (1 - discount)

        processed_results.append({
            'order_id': order['id'], 
            'total_price': round(current_order_total, 2)
        })

    return processed_results