import logging
import os

# 1. Definir la ruta de la carpeta de logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 2. Crear la carpeta si no existe (esto evita el FileNotFoundError)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 3. Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE,
    encoding='utf-8' # Buena práctica en Python 3.14
)

logger = logging.getLogger("CollabTaskAPI")