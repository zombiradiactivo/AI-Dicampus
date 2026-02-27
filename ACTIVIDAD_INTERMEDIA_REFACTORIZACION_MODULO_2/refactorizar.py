from abc import ABC, abstractmethod

# --- Estrategias (Algoritmos de descuento) ---

class EstrategiaDescuento(ABC):
    @abstractmethod
    def calcular(self, precio: float, cantidad: int, estado: int) -> float:
        pass

class DescuentoClienteA(EstrategiaDescuento):
    def calcular(self, precio, cantidad, estado):
        # Solo suma si el estado es 1
        return precio * cantidad if estado == 1 else 0

class DescuentoClienteB(EstrategiaDescuento):
    def calcular(self, precio, cantidad, estado):
        subtotal = precio * cantidad
        if estado == 1:
            return subtotal * 0.9
        if estado == 2:
            return subtotal * 0.8
        return 0

class DescuentoGeneral(EstrategiaDescuento):
    def calcular(self, precio, cantidad, estado):
        return precio * cantidad

# --- Contexto y Orquestación ---

class ProcesadorPedidos:
    def __init__(self, estrategia: EstrategiaDescuento):
        self.estrategia = estrategia

    def calcular_total(self, productos, descuento_final_pct=0):
        total = sum(
            self.estrategia.calcular(p['p'], p['q'], p['s']) 
            for p in productos
        )
        
        if descuento_final_pct > 0:
            total -= (total * descuento_final_pct / 100)
            
        return total

# --- Uso del código ---

# Mapeo de tipos a estrategias
ESTRATEGIAS = {
    'A': DescuentoClienteA(),
    'B': DescuentoClienteB()
}

def obtener_total_pedido(datos, tipo_cliente, desc_extra=0):
    # Obtiene la estrategia o usa la general por defecto
    estrategia = ESTRATEGIAS.get(tipo_cliente, DescuentoGeneral())
    procesador = ProcesadorPedidos(estrategia)
    return procesador.calcular_total(datos, desc_extra)