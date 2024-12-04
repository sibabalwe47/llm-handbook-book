
from zenml.logger import get_logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from zenml.client import Client
from zenml.exceptions import EntityExistsError
from urllib.parse import quote_plus
username = ""
password = ""
encoded_password = quote_plus(password)



logger = get_logger(__name__)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


    # OpenAI API

    # Huggingface API

    # Comet ML (during training)

    # MongoDB database
    DATABASE_HOST: str = "mongodb+srv://{username}:{encoded_password}@langgraph.ofbab.mongodb.net/?retryWrites=true&w=majority&appName=langgraph"
    DATABASE_NAME: str = "twin"


    @classmethod
    def load_settings(cls) -> "Settings":
        try:
            logger.info("Loading settings from the ZenML secret store.")
            settings_secrets = Client().get_secret("settings")
            settings = Settings(**settings_secrets.secret_values)
        except (RuntimeError, KeyError):
            logger.warning(
                "Failed to load settings from the ZenML secret store. Defaulting to loading the settings from the '.env' file."
            )

            settings = Settings()

        return settings
    
settings = Settings.load_settings()