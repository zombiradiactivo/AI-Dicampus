from abc import ABC, abstractmethod
from typing import List, Dict, TypedDict, Optional

# --- 1. MODELOS (Define las estructuras para que Pylance esté feliz) ---

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

# --- 2. INFRAESTRUCTURA (Responsabilidad: Gestión de Datos) ---

class InventoryManager:
    """Se encarga exclusivamente de la búsqueda y validación de productos."""
    def __init__(self, inventory_data: List[Product]):
        self._registry = {p['id']: p for p in inventory_data}

    def get_product(self, product_id: int) -> Optional[Product]:
        product = self._registry.get(product_id)
        if not product:
            print(f"ALERTA: Producto {product_id} no existe.")
            return None
        if product['stock'] <= 0:
            return None
        return product

# --- 3. ESTRATEGIAS (Mantenemos el patrón del paso anterior) ---

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float, items_count: int, rate: float) -> float: ...

class PremiumDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate)

class VIPDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        final = total * (1 - rate)
        return final * 0.95 if final > 1000 else final

class BulkDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate) if items_count > 10 else total

class NoDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total

# --- 4. ORQUESTADOR (Procesador de Pedidos) ---

class OrderProcessor:
    STRATEGIES = {
        'premium': PremiumDiscount(),
        'vip': VIPDiscount(),
        'bulk': BulkDiscount()
    }

    def __init__(self, inventory_manager: InventoryManager, discount_rates: Dict[str, float]):
        self.inventory = inventory_manager
        self.rates = discount_rates

    def process_all(self, orders: List[Order]) -> List[Dict]:
        return [self._process_single_order(o) for o in orders]

    def _process_single_order(self, order: Order) -> Dict:
        # Cálculo de subtotal
        subtotal = 0.0
        for item in order['items']:
            product = self.inventory.get_product(item['id'])
            if product:
                subtotal += item['qty'] * product['price']

        # Aplicación de descuento
        order_type = order.get('type', 'default')
        strategy = self.STRATEGIES.get(order_type, NoDiscount())
        rate = self.rates.get(order_type, 0.0)

        final_total = strategy.apply(subtotal, len(order['items']), rate)

        return {
            'order_id': order['id'],
            'total': round(final_total, 2)
        }