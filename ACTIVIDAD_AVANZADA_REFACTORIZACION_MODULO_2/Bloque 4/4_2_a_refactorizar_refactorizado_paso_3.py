from abc import ABC, abstractmethod
from typing import List, Dict, TypedDict

# --- INFRAESTRUCTURA DEL PATRÓN STRATEGY ---

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float, items_count: int, rate: float) -> float:
        pass

class PremiumDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total * (1 - rate)

class VIPDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        final_total = total * (1 - rate)
        # Regla de negocio específica: bono adicional por volumen
        if final_total > 1000:
            final_total *= 0.95
        return final_total

class BulkDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        if items_count > 10:
            return total * (1 - rate)
        return total

class NoDiscount(DiscountStrategy):
    def apply(self, total: float, items_count: int, rate: float) -> float:
        return total

# Mapeo de estrategias (Fácil de extender sin tocar la lógica principal)
STRATEGIES = {
    'premium': PremiumDiscount(),
    'vip': VIPDiscount(),
    'bulk': BulkDiscount()
}

# --- FUNCIÓN PRINCIPAL REFACTORIZADA ---

def process_orders(
    orders: List[Order],                # type: ignore
    discount_rates: Dict[str, float], 
    inventory_data: List[Product]       # type: ignore
) -> List[Dict]:
    
    inventory_registry = {product['id']: product for product in inventory_data}
    processed_results = []

    for order in orders:
        current_order_total = 0.0
        
        # 1. Cálculo de base (Subtotal)
        for item in order['items']:
            product = inventory_registry.get(item['id'])
            if product and product['stock'] > 0:
                current_order_total += item['qty'] * product['price']

        # 2. Aplicación de Estrategia (Eliminamos el bloque if/elif)
        order_type = order.get('type', 'default')
        strategy = STRATEGIES.get(order_type, NoDiscount())
        rate = discount_rates.get(order_type, 0.0)
        
        final_total = strategy.apply(
            total=current_order_total, 
            items_count=len(order['items']), 
            rate=rate
        )

        processed_results.append({
            'order_id': order['id'], 
            'total_price': round(final_total, 2)
        })

    return processed_results