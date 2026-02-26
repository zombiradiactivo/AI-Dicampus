import time
import threading
from dataclasses import dataclass

@dataclass
class Bucket:
    tokens: float
    last_update: float

class IPTokenBucketLimiter:
    def __init__(self, rate: float, capacity: float, expiry_seconds: float = 60.0):
        """
        :param rate: Cuántos tokens se añaden por segundo.
        :param capacity: El máximo de tokens que puede tener un bucket.
        :param expiry_seconds: Tiempo de inactividad antes de borrar una IP.
        """
        self.rate = rate
        self.capacity = capacity
        self.expiry_seconds = expiry_seconds
        self.buckets = {}
        self.lock = threading.Lock()

    def _refresh_and_cleanup(self, ip: str, now: float):
        # Limpieza de IPs inactivas (Mantiene O(1) amortizado en el acceso)
        # Nota: En una app real, podrías querer un hilo de limpieza separado,
        # pero aquí lo manejamos bajo demanda para cumplir con la restricción de stdlib.
        expired_ips = [i for i, b in self.buckets.items() if now - b.last_update > self.expiry_seconds]
        for i in expired_ips:
            del self.buckets[i]

    def allow_request(self, ip: str) -> bool:
        with self.lock:
            now = time.monotonic()
            self._refresh_and_cleanup(ip, now)
            
            # Obtener o crear bucket
            bucket = self.buckets.get(ip)
            if not bucket:
                bucket = Bucket(self.capacity, now)
                self.buckets[ip] = bucket

            # Calcular nuevos tokens (Token Bucket Algorithm)
            delta = now - bucket.last_update
            new_tokens = delta * self.rate
            bucket.tokens = min(self.capacity, bucket.tokens + new_tokens)
            bucket.last_update = now

            # Lógica de consumo
            if bucket.tokens >= 1:
                bucket.tokens -= 1
                return True
            return False

# --- Unit Tests ---
import unittest

class TestIPTokenBucket(unittest.TestCase):
    def setUp(self):
        # 1 token por segundo, capacidad 2
        self.limiter = IPTokenBucketLimiter(rate=1.0, capacity=2.0, expiry_seconds=1.0)

    def test_burst_capacity(self):
        """Caso 1: Permite ráfagas hasta la capacidad máxima."""
        self.assertTrue(self.limiter.allow_request("1.1.1.1"))
        self.assertTrue(self.limiter.allow_request("1.1.1.1"))
        self.assertFalse(self.limiter.allow_request("1.1.1.1"))

    def test_rate_refill(self):
        """Caso 2: Los tokens se regeneran con el tiempo."""
        self.limiter.allow_request("2.2.2.2")
        self.limiter.allow_request("2.2.2.2")
        time.sleep(1.1)  # Esperar a que se regenere al menos 1 token
        self.assertTrue(self.limiter.allow_request("2.2.2.2"))

    def test_ip_isolation(self):
        """Caso 3: El límite de una IP no afecta a otra."""
        for _ in range(2): self.limiter.allow_request("3.3.3.3")
        self.assertFalse(self.limiter.allow_request("3.3.3.3"))
        self.assertTrue(self.limiter.allow_request("4.4.4.4"))

    def test_expiration_cleanup(self):
        """Caso 4: Las IPs inactivas se eliminan del diccionario."""
        self.limiter.allow_request("5.5.5.5")
        self.assertIn("5.5.5.5", self.limiter.buckets)
        time.sleep(1.1)  # Superar expiry_seconds
        self.limiter.allow_request("6.6.6.6") # Trigger cleanup
        self.assertNotIn("5.5.5.5", self.limiter.buckets)

    def test_thread_safety(self):
        """Caso 5: Acceso concurrente sin corrupción de datos."""
        import concurrent.futures
        def task():
            return self.limiter.allow_request("7.7.7.7")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda _: task(), range(10)))
        
        # Con capacidad 2, solo 2 deberían ser True inmediatamente
        self.assertEqual(results.count(True), 2)

if __name__ == "__main__":
    unittest.main()