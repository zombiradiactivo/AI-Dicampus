### Todos los archivos separados estan aqui https://github.com/zombiradiactivo/AI-Dicampus/tree/main/ACTIVIDAD_FUNCIONES_SIMPLES

def es_positivo (numero):
    return numero > 0

def capitalizar(texto):
    if texto:
        capitalizado = texto.title()
        return capitalizado
    else:
        return "Nombre Vacio"

def validar_email(email):
    if '@' in email and '.' in email:
        return True
    else:
        return False

def resumen_usuario(nombre, email):
    nombre_capitalizado = capitalizar(nombre)
    if validar_email(email) is True:
        print("Usuario:",(nombre_capitalizado), " --  Email correcto")
    else:
        print("Usuario:" ,(nombre_capitalizado) , " --  Email invalido")

## Testing

if __name__ == "__main__":
    
    print("\n")
    print("-" * 10)
    print("Testing Numeros positivos")
    print("-" * 10)

    print(es_positivo(5))                   # True
    print(es_positivo(-8))                  # False
    print(es_positivo(64216))               # True

    print("\n")
    print("-" * 10)
    print("Testing Capitalizar Palabras")
    print("-" * 10)

    print(capitalizar("hola mundo"))        # Hola Mundo
    print(capitalizar(""))                  # Nombre Vacio

    print("\n")
    print("-" * 10)
    print("Testing Validar Email")
    print("-" * 10)

    print(validar_email("test@test.com"))   # True
    print(validar_email("testtest.com"))    # False
    print(validar_email("test@testcom"))    # False
    print(validar_email("testtestcom"))     # False

    print("\n")
    print("-" * 10)
    print("Testing Resumen Usuario")
    print("-" * 10)

    resumen_usuario("andres","andres@test.com")         # Usuario: Andres  --  Email correcto
    resumen_usuario("","andres@test.com")               # Usuario: Nombre Vacio  --  Email correcto
    resumen_usuario("andres lopez","andrestest.com")    # Usuario: Andres Lopez  --  Email invalido
    resumen_usuario("andres lopez","andres@testcom")    # Usuario: Andres Lopez  --  Email invalido
    resumen_usuario("andres lopez","andrestestcom")     # Usuario: Andres Lopez  --  Email invalido
    resumen_usuario("","andrestestcom")                 # Usuario: Nombre Vacio  --  Email invalido