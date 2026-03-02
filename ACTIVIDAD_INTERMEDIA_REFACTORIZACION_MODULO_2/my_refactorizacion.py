class Procesador:
    def __init__(self, data):
        self.data = data

    def ejecutar(self):
        for d in self.data:
            if d[1] > 3000:
                s = d[1] * 1.1
            else:
                s = d[1] * 1.05
            
            print("--- Reporte ---")
            print("Nombre: " + d[0])
            print("Salario final: " + str(s))
            
            if d[2] == "Senior":
                b = s * 0.2
                print("Bonus: " + str(b))
                print("Total: " + str(s + b))
            else:
                b = s * 0.05
                print("Bonus: " + str(b))
                print("Total: " + str(s + b))
            print("---------------")

# Ejemplo de uso con Data Clumps (los datos pasan como una lista cruda sin estructura)
p = Procesador([["Alex", 4000, "Senior"], ["Santi", 2500, "Junior"]])
p.ejecutar()