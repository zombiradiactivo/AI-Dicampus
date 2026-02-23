class Usuario:
    """
    Representa a un usuario dentro del sistema de gestión.

    Esta clase centraliza la información básica de los perfiles de usuario
    y permite gestionar su estado de actividad y contacto.

    Attributes:
        nombre (str): Nombre completo del usuario.
        edad (int): Edad actual del usuario en años.
        email (str): Dirección de correo electrónico principal.
        activo (bool): Indica si la cuenta del usuario está operativa.
    """

    def __init__(self, nombre, edad, email):
        """
        Inicializa una nueva instancia de la clase Usuario.

        Args:
            nombre (str): Nombre completo del usuario.
            edad (int): Edad del usuario (debe ser un entero positivo).
            email (str): Dirección de correo electrónico válida.

        Returns:
            None: El constructor no retorna un valor.
        """
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.activo = True

    def cambiar_email(self, nuevo_email):
        """
        Actualiza la dirección de correo electrónico del usuario.

        Valida de forma básica que el string contenga un carácter '@' antes
        de proceder con la actualización.

        Args:
            nuevo_email (str): La nueva dirección de correo a registrar.

        Returns:
            bool: True si el email se actualizó correctamente, 
                  False si el formato no es válido.
        """
        if "@" in nuevo_email:
            self.email = nuevo_email
            return True
        return False

    def desactivar(self):
        """
        Cambia el estado del usuario a inactivo.

        Este método modifica el atributo `activo` a False, restringiendo
        (teóricamente) el acceso del usuario al sistema.

        Returns:
            bool: Siempre retorna True para confirmar que la operación se completó.
        """
        self.activo = False
        return True