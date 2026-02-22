from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    """
    Application setting and environment variable management. 
    Pydantic automatically validates that required variables are present.
    """

    # Database connection string
    # If 'DATABASE_URL' missing from .env the application will raise an error on startup. 
    database_url: str 

    # Local storage dictory for uploaded files, defaulting to "./data" if not set in environment variables
    data_dir: str = "./data" 

    # Pydantic configuration for settings management
    # env_file tells pydantic to look for variables in a file named ".evn" 
    # extra="ignore" ignore any variables in the .env file that are not defined in this Settings class.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() 