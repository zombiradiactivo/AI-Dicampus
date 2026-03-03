import time
import threading
from collections import OrderedDict
from functools import wraps

class CacheManager:
    def __init__(self, max_size=100):
        self._cache = OrderedDict()  # Para política LRU
        self._hits = 0
        self._misses = 0
        self._max_size = max_size
        self._lock = threading.Lock() # Para entornos multi-hilo

    def cached(self, ttl=300):
        """
        Decorador para envolver funciones de base de datos.
        Permite configurar el TTL por cada función distinta.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(key, *args, **kwargs):
                now = time.time()
                
                with self._lock:
                    # 1. Intento de Hit
                    if key in self._cache:
                        data, expires_at = self._cache[key]
                        if now < expires_at:
                            self._hits += 1
                            # Mover al final (marcar como usado recientemente)
                            self._cache.move_to_end(key)
                            return data
                        else:
                            # Expirado
                            del self._cache[key]

                    # 2. Cache Miss
                    self._misses += 1
                
                # Ejecutamos la función externa fuera del lock para no bloquear hilos
                # mientras la DB responde (I/O)
                result = func(key, *args, **kwargs)

                with self._lock:
                    # 3. Política de Expulsión (LRU)
                    if len(self._cache) >= self._max_size:
                        # Elimina el primer elemento (el menos usado recientemente)
                        self._cache.popitem(last=False)

                    # 4. Guardado con TTL individual
                    self._cache[key] = (result, now + ttl)
                    
                return result
            return wrapper
        return decorator

    def get_stats(self):
        with self._lock:
            total = self._hits + self._misses
            ratio = self._hits / total if total > 0 else 0.0
            return {
                "hits": self._hits,
                "misses": self._misses,
                "ratio": f"{ratio:.2%}",
                "current_size": len(self._cache)
            }

# --- Ejemplo de Uso ---

# Instancia única (puedes usarla como Singleton)
db_cache = CacheManager(max_size=500)

@db_cache.cached(ttl=60) # TTL específico para esta función
def fetch_from_db(key):
    # Simula una operación costosa de DB
    print(f"--- Consultando DB para: {key} ---")
    time.sleep(0.1) 
    return f"Data for {key}"

# Pruebas
if __name__ == "__main__":
    # Primer acceso (Miss)
    print(fetch_from_db("user_1"))
    
    # Segundo acceso (Hit)
    print(fetch_from_db("user_1"))
    
    print(db_cache.get_stats())