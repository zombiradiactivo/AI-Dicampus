from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Añadimos tipos opcionales o valores por defecto para evitar el error de instanciación
    SECRET_KEY: str = "desarrollo_secret_key_temporal" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # Configuración del archivo .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variables extra en el .env que no estén aquí
    )

# Ahora no dará error al instanciar
settings = Settings()