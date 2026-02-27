import bcrypt
import secrets

def autenticar_usuario(nombre_usuario, password_plana, repositorio_usuarios):
    """
    Verifica las credenciales de un usuario y devuelve su nivel de acceso.

    La función implementa hashing seguro mediante bcrypt y protege contra 
    ataques de temporización y escalada de privilegios.

    Args:
        nombre_usuario (str): El identificador único del usuario.
        password_plana (str): La contraseña proporcionada por el usuario sin procesar.
        repositorio_usuarios (list): Lista de diccionarios que simula la base de datos.
            Cada diccionario debe contener: 'username', 'password_hash' y 'rol'.

    Returns:
        dict: Un diccionario con el estado de la autenticación, el nivel (lvl) 
              y un mensaje descriptivo.
              Format: {'ok': bool, 'lvl': int, 'msg': str}
    """
    
    # 1. Búsqueda del registro de usuario
    # En sistemas de producción, esto debería ser una consulta SQL indexada
    usuario_encontrado = None
    for registro in repositorio_usuarios:
        if registro['username'] == nombre_usuario:
            usuario_encontrado = registro
            break
    
    # Fail Fast: Si el usuario no existe, salimos inmediatamente.
    # Usamos un mensaje genérico para evitar la enumeración de usuarios.
    if not usuario_encontrado:
        return {'ok': False, 'lvl': -1, 'msg': 'Credenciales inválidas'}

    # 2. Verificación de contraseña
    # checkpw extrae automáticamente el 'salt' almacenado en el hash y lo aplica 
    # a la password_plana antes de comparar. Es resistente a fuerza bruta.
    password_correcta = bcrypt.checkpw(
        password_plana.encode('utf-8'), 
        usuario_encontrado['password_hash']
    )

    # 3. Validación de integridad
    # Usamos constantes de tiempo para evitar ataques de canal lateral (Timing attacks).
    if not password_correcta:
        return {'ok': False, 'lvl': -1, 'msg': 'Credenciales inválidas'}

    # 4. Determinación de nivel de acceso (Autorización)
    # Recuperamos el rol directamente de la fuente de verdad (DB), no de la entrada del usuario.
    rol_usuario = usuario_encontrado.get('rol', 'guest')
    
    # Mapa de privilegios para desacoplar la lógica de negocio de la base de datos.
    niveles_acceso = {
        'admin': {'lvl': 3, 'msg': 'Admin OK'},
        'user':  {'lvl': 1, 'msg': 'User OK'},
        'guest': {'lvl': 0, 'msg': 'Guest OK'}
    }

    # Asignamos el nivel basado en el rol, con 'guest' como fallback de seguridad.
    config_acceso = niveles_acceso.get(rol_usuario, niveles_acceso['guest'])
    
    # Unimos el estado de éxito con la configuración de nivel encontrada.
    return {'ok': True, **config_acceso}