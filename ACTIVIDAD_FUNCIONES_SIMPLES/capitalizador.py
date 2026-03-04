def capitalizar(texto):
    if texto:
        capitalizado = texto.title()
        if __name__ == "__main__":
            print (capitalizado)
        return capitalizado
    else: 
        if __name__ == "__main__":
            print ("Texto vacio")
        return "Nombre Vacio"


if __name__ == "__main__":
    capitalizar("hola mundo")
    print ("\n-------\n")
    capitalizar("")