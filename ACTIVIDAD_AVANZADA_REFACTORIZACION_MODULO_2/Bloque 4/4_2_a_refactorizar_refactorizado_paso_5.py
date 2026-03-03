from abc import ABC, abstractmethod
from typing import List, Dict, TypedDict, Optional

# --- 1. MODELOS DE DATOS (Modernización y Tipado) ---

class OrderItem(TypedDict):
    id: int
    qty: int

class Order(TypedDict):
    id: int
    type: str  # 'premium', 'vip', 'bulk', 'default'
    items: List[OrderItem]

class Product(TypedDict):
    id: int
    stock: int
    price: float

# --- 2. INFRAESTRUCTURA DE INVENTARIO (Modularización - SRP) ---

class InventoryManager:
    """Responsable exclusivamente de la gestión y búsqueda de productos."""
    
    def __init__(self, inventory_data: List[Product]):
        # Paso 1: Optimización O(n^2) -> O(n) mediante indexación
        self._registry = {p['id']: p for p in inventory_data}

    def get_product(self, product_id: int) -> Optional[Product]:
        product = self._registry.get(product_id)
        
        # Paso 5: Cláusulas de guarda (Simplificación de condicionales)
        if not product:
            print(f"ALERTA: Producto {product_id} no encontrado.")
            return None
            
        if product['stock'] <= 0:
            print(f"ALERTA: Producto {product_id} sin existencias.")
            return None
            
        return product

# --- 3. PATRÓN STRATEGY PARA DESCUENTOS (Patrón de Diseño) ---

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float, items_count: int, rate: float) -> float:
        """Aplica la lógica de descuento específica."""
        pass

class PremiumDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate)

class VIPDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        discounted_total = total * (1 - rate)
        # Regla VIP: 5% extra si supera los 1000
        return discounted_total * 0.95 if discounted_total > 1000 else discounted_total

class BulkDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        # Cláusula de guarda: solo aplica si hay más de 10 items
        if items_count <= 10:
            return total
        return total * (1 - rate)

class NoDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total

# --- 4. PROCESADOR DE PEDIDOS (Orquestador) ---

class OrderProcessor:
    # Registro de estrategias disponibles
    STRATEGIES = {
        'premium': PremiumDiscount(),
        'vip': VIPDiscount(),
        'bulk': BulkDiscount()
    }

    def __init__(self, inventory_manager: InventoryManager, discount_rates: Dict[str, float]):
        self.inventory = inventory_manager
        self.rates = discount_rates

    def process_all(self, orders: List[Order]) -> List[Dict]:
        """Procesa una lista de pedidos y devuelve los totales calculados."""
        return [self._process_single_order(o) for o in orders]

    def _process_single_order(self, order: Order) -> Dict:
        subtotal = 0.0
        
        # Cálculo de base
        for item in order['items']:
            product = self.inventory.get_product(item['id'])
            
            # Paso 5: Uso de 'continue' para evitar anidación
            if not product:
                continue
                
            subtotal += item['qty'] * product['price']

        # Selección dinámica de estrategia
        order_type = order.get('type', 'default')
        strategy = self.STRATEGIES.get(order_type, NoDiscount())
        rate = self.rates.get(order_type, 0.0)

        # Aplicación del descuento
        final_total = strategy.apply(
            total=subtotal, 
            items_count=len(order['items']), 
            rate=rate
        )

        return {
            'order_id': order['id'],
            'total': round(final_total, 2)
        }

# --- EJEMPLO DE USO ---

if __name__ == "__main__":
    # Datos de entrada
    inventory = [
        {"id": 1, "stock": 10, "price": 100.0},
        {"id": 2, "stock": 0, "price": 50.0},
        {"id": 3, "stock": 5, "price": 200.0}
    ]
    
    discounts = {"premium": 0.1, "vip": 0.2, "bulk": 0.15}
    
    orders = [
        {"id": 101, "type": "premium", "items": [{"id": 1, "qty": 2}]},
        {"id": 102, "type": "vip", "items": [{"id": 3, "qty": 10}]}, # Supera 1000
    ]

    # Ejecución
    inv_manager = InventoryManager(inventory)       # type: ignore
    processor = OrderProcessor(inv_manager, discounts)
    
    final_results = processor.process_all(orders)   # type: ignore
    print(final_results)