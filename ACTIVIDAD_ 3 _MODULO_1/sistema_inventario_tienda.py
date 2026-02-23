import json
import os

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }

    def __str__(self):
        return f"Producto: {self.nombre.ljust(15)} | Precio: ${self.precio:>8.2f} | Stock: {self.cantidad:>4}"

class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = self.cargar_desde_archivo()

    def agregar_producto(self, nombre, precio, cantidad):
        nuevo_p = Producto(nombre, precio, cantidad)
        self.productos.append(nuevo_p)
        print(f"✅ '{nombre}' agregado correctamente.")

    def eliminar_producto(self, nombre):
        original_count = len(self.productos)
        self.productos = [p for p in self.productos if p.nombre.lower() != nombre.lower()]
        if len(self.productos) < original_count:
            print(f"🗑️ '{nombre}' eliminado.")
        else:
            print(f"⚠️ No se encontró el producto '{nombre}'.")

    def buscar_producto(self, nombre):
        encontrados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]
        return encontrados

    def listar_productos(self):
        if not self.productos:
            print("📭 El inventario está vacío.")
        else:
            print("\n--- Lista de Inventario ---")
            for p in self.productos:
                print(p)

    def calcular_valor_total(self):
        # Usamos la fórmula: Valor = Suma de (precio * cantidad)
        total = sum(p.precio * p.cantidad for p in self.productos)
        return total

    def guardar_en_archivo(self):
        with open(self.archivo, 'w') as f:
            json.dump([p.to_dict() for p in self.productos], f, indent=4)
        print(f"💾 Inventario guardado en '{self.archivo}'.")

    def cargar_desde_archivo(self):
        if not os.path.exists(self.archivo):
            return []
        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                return [Producto(d['nombre'], d['precio'], d['cantidad']) for d in datos]
        except (json.JSONDecodeError, KeyError):
            print("❌ Error al leer el archivo. Iniciando inventario vacío.")
            return []

# --- Ejemplo de uso ---
def menu():
    mi_tienda = Inventario()
    
    # Agregar algunos productos de prueba
    if not mi_tienda.productos:
        mi_tienda.agregar_producto("Café", 12.50, 50)
        mi_tienda.agregar_producto("Leche", 2.10, 100)
    
    mi_tienda.listar_productos()
    print(f"\n💰 Valor Total: ${mi_tienda.calcular_valor_total():.2f}")
    
    # Guardar cambios
    mi_tienda.guardar_en_archivo()

if __name__ == "__main__":
    menu()