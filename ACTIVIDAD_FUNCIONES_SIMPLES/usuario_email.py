from capitalizador import capitalizar ## Archivo capitalizador.py
from validador_email import validar_email ## Archivo validador_email.py

def resumen_usuario(nombre, email):
    nombre_capitalizado = capitalizar(nombre)
    if validar_email(email) is True:
        print("Usuario:",(nombre_capitalizado), " --  Email correcto")
    else:
        print("Usuario:" ,(nombre_capitalizado) , " --  Email invalido")
        
if __name__ == "__main__":
    resumen_usuario("andres","andres@test.com")
    resumen_usuario("","andres@test.com")
    resumen_usuario("andres lopez","andrestest.com")
    resumen_usuario("andres lopez","andres@testcom")
    resumen_usuario("andres lopez","andrestestcom")
    resumen_usuario("","andrestestcom")