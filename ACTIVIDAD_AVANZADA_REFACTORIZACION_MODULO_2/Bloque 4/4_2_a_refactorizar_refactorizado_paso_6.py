from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Sequence

# --- 1. MODELOS DE DATOS (Modernización con Dataclasses) ---
# Usamos slots=True para mejor rendimiento y memoria

@dataclass(frozen=True, slots=True)
class OrderItem:
    id: int
    qty: int

@dataclass(frozen=True, slots=True)
class Order:
    id: int
    order_type: str  # 'premium', 'vip', 'bulk', 'default'
    items: List[OrderItem]

@dataclass(slots=True)
class Product:
    id: int
    stock: int
    price: float

# --- 2. INFRAESTRUCTURA DE INVENTARIO (SRP) ---

class InventoryManager:
    def __init__(self, inventory_data: Sequence[Product]):
        # Indexación O(n) para búsquedas O(1)
        self._registry: Dict[int, Product] = {p.id: p for p in inventory_data}

    def get_product(self, product_id: int) -> Optional[Product]:
        product = self._registry.get(product_id)
        
        if not product:
            print(f"ALERTA: Producto {product_id} no encontrado.")
            return None
            
        if product.stock <= 0:
            print(f"ALERTA: Producto {product_id} sin existencias.")
            return None
            
        return product

# --- 3. PATRÓN STRATEGY (Diseño) ---

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float, items_count: int, rate: float) -> float:
        pass

class PremiumDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate)

class VIPDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        discounted = total * (1 - rate)
        return discounted * 0.95 if discounted > 1000 else discounted

class BulkDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate) if items_count > 10 else total

class NoDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total

# --- 4. PROCESADOR DE PEDIDOS (Orquestación) ---

class OrderProcessor:
    _STRATEGIES: Dict[str, DiscountStrategy] = {
        'premium': PremiumDiscount(),
        'vip': VIPDiscount(),
        'bulk': BulkDiscount()
    }

    def __init__(self, inventory: InventoryManager, discount_rates: Dict[str, float]):
        self.inventory = inventory
        self.rates = discount_rates

    def process_all(self, orders: Sequence[Order]) -> List[Dict]:
        return [self._process_single_order(o) for o in orders]

    def _process_single_order(self, order: Order) -> Dict:
        subtotal = 0.0
        
        for item in order.items:
            product = self.inventory.get_product(item.id)
            if product:
                subtotal += item.qty * product.price

        strategy = self._STRATEGIES.get(order.order_type, NoDiscount())
        rate = self.rates.get(order.order_type, 0.0)

        final_total = strategy.apply(subtotal, len(order.items), rate)

        return {
            'order_id': order.id,
            'total': round(final_total, 2)
        }

# --- EJEMPLO DE USO (Sin errores de Pylance) ---

if __name__ == "__main__":
    # Ahora creamos objetos reales, no diccionarios "desnudos"
    inventory = [
        Product(id=1, stock=10, price=100.0),
        Product(id=2, stock=0, price=50.0),
        Product(id=3, stock=5, price=200.0)
    ]
    
    discounts = {"premium": 0.1, "vip": 0.2, "bulk": 0.15}
    
    orders = [
        Order(id=101, order_type="premium", items=[OrderItem(id=1, qty=2)]),
        Order(id=102, order_type="vip", items=[OrderItem(id=3, qty=10)]),
    ]

    inv_manager = InventoryManager(inventory)
    processor = OrderProcessor(inv_manager, discounts)
    
    print(processor.process_all(orders))