# from typing import Optional, List 
# from dataclasses import dataclass 
# from datetime import datetime

# @dataclass
# class Transaction: 
#     id: str 
#     amount: float 
#     currency: str
#     timestamp: datetime 
#     category: str
#     description: Optional[str] = None

# def analyze_spending(
#     transactions: List[Transaction], 
#     month: int,
#     year: int,
#     currency: str = 'EUR'
# ) -> dict:
#     """
#     Analiza gastos mensuales agrupados por categoría. 
#     Filtra por mes/año y convierte a moneda base.
#     Raises ValueError si transactions está vacío. 
#     """
#     if not transactions:
#         raise ValueError('Lista de transacciones vacía')
#     ...


from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

@dataclass
class Transaction: 
    id: str 
    amount: float 
    currency: str
    timestamp: datetime 
    category: str
    description: Optional[str] = None

def analyze_spending(
    transactions: List[Transaction], 
    month: int,
    year: int,
    base_currency: str = 'EUR'
) -> Dict[str, float]:
    """
    Analiza gastos mensuales agrupados por categoría. 
    Filtra por mes/año y convierte a moneda base (simulado).
    
    Raises:
        ValueError: Si la lista de transacciones está vacía o el mes es inválido.
    """
    if not transactions:
        raise ValueError('Lista de transacciones vacía')
    
    if not (1 <= month <= 12):
        raise ValueError('Mes no válido. Debe estar entre 1 y 12')

    # Diccionario de tasas de cambio simulado (Relación respecto a EUR)
    exchange_rates = {
        'EUR': 1.0,
        'USD': 0.92,
        'GBP': 1.17,
        'JPY': 0.006
    }

    # Diccionario para agrupar gastos: clave=categoría, valor=suma acumulada
    spending_by_category = defaultdict(float)
    found_data = False

    for tx in transactions:
        # 1. Filtrado por mes y año
        if tx.timestamp.month == month and tx.timestamp.year == year:
            found_data = True
            
            # 2. Conversión de moneda a la moneda base
            # Obtenemos la tasa de la moneda original o 1.0 si no existe
            rate_to_eur = exchange_rates.get(tx.currency, 1.0)
            target_rate = exchange_rates.get(base_currency, 1.0)
            
            # Convertimos el monto a la moneda base solicitada
            amount_in_base = (tx.amount * rate_to_eur) / target_rate
            
            # 3. Agrupación por categoría
            spending_by_category[tx.category] += round(amount_in_base, 2)

    # 4. Manejo de meses sin datos
    if not found_data:
        print(f"Aviso: No se encontraron transacciones para {month}/{year}.")
        return {}

    return dict(spending_by_category)

# --- Ejemplo de uso ---
if __name__ == "__main__":
    data = [
        Transaction("1", 50.0, "EUR", datetime(2023, 5, 10), "Comida"),
        Transaction("2", 20.0, "USD", datetime(2023, 5, 15), "Transporte"),
        Transaction("3", 100.0, "EUR", datetime(2023, 5, 20), "Comida"),
        Transaction("4", 200.0, "EUR", datetime(2023, 6, 1), "Alquiler")
    ]

    try:
        resultado = analyze_spending(data, 5, 2023)
        print("Resumen de gastos por categoría (EUR):", resultado)
    except ValueError as e:
        print(f"Error: {e}")