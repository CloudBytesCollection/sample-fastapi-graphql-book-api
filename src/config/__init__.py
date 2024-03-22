from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Book API"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = ""
    DB_NAME: str = ""


class InfrastructureSettings(BaseSettings):
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_ACCOUNT: str = ""  # Your AWS Account #
    AWS_REGION: str = ""  # Example: us-east-1
    ENV_TYPE: str = "Dev"  # Examples: Dev, Staging, Prod
    DOMAIN_NAME: str = ""  # No www. Format Expected: example.com
    LOCAL_NETWORK_CIDR: str = ""  # CIDR Format Expected: 0.0.0.0/32


class Settings(
    CommonSettings, ServerSettings, DatabaseSettings, InfrastructureSettings
):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
