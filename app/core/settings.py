from typing import Literal, Tuple

from psutil import disk_usage, cpu_percent, virtual_memory
from pydantic import Field, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app import __version__


class Settings(BaseSettings):
    """Settings _summary_

    _extended_summary_

    :param BaseSettings: _description_
    :type BaseSettings: _type_
    :return: _description_
    :rtype: _type_
    """

    # Project Configuration
    API_VERSION: str = Field(__version__)
    PROJECT_NAME: str = Field("Default Project Name")
    PROJECT_DESCRIPTION: str = Field("Default Project Description")
    ENV: Literal["local", "development", "production"] = Field("development")
    HOST: str = Field("0.0.0.0")  # noqa: S104
    PORT: int = Field(8087)
    DEBUG: bool = Field(False)  # noqa: FBT003
    ALLOWED_CORS_ORIGIN: str | list[Literal["*"] | AnyHttpUrl] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # Database Configuration and Authentication Configurations
    DATABASE_URL: str = Field("sqlite:///./app.db")
    DB_TYPE: str = Field("sqlite")
    JWT_SECRET_KEY: str = Field("default_secret_key")
    JWT_REFRESH_SECRET_KEY: str = Field("default_refresh_secret_key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    MAINTAINERS_EMAILS: str = Field("luisangelmarcia@gmail.com")

    # Timeouts and intervals of delays
    DEFAULT_TIMEOUT: int = Field(300)
    SHORT_INTERVAL: int = Field(36)
    LONG_INTERVAL: int = Field(72)

    # Logger Settings
    LOGGER_LEVEL: str = Field("INFO")
    LOGGER_FORMAT: str = Field(
        "%(asctime)s - line:%(lineno)d - %(name)s - %(levelname)s - %(message)s - %(funcName)s - %(pathname)s",
    )
    LOGGER_FILE_NAME: str = Field("/tmp/logger.log")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def check_env_variables(self) -> str:
        """check_env_variables _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        env_variables_str = ""

        temp_dict_keys = self.model_dump()

        for env_variable in temp_dict_keys:
            env_variables_str += f"{env_variable}: {getattr(self, env_variable)}\n"

        return env_variables_str

    @property
    def get_db_client(self) -> AsyncIOMotorClient | None:
        """get_db_client _summary_

        _extended_summary_

        :return: _description_
        :rtype: _type_
        """
        db_client = None
        if self.DB_TYPE == "mongodb":
            db_client = AsyncIOMotorClient(self.DATABASE_URL, uuidRepresentation="standard")

        elif self.DB_TYPE == "sqlite":
            # SQLite initialization logic can be added here if needed | TODO: <CosmicTiger>: Pending implementation
            db_client = None
        return db_client

    @property
    def get_database(self) -> AsyncIOMotorDatabase | None:
        """get_database _summary_

        _extended_summary_

        :return: _description_
        :rtype: _type_
        """
        db_client = self.get_db_client
        if db_client and self.DB_TYPE == "mongodb":
            return db_client.get_default_database()
        return None

    @property
    async def get_ping_pong_db(self) -> bool:
        """get_ping_pong_db _summary_

        _extended_summary_

        :return: _description_
        :rtype: bool
        """
        database = self.get_database
        if database is not None and self.DB_TYPE == "mongodb":
            try:
                pong = await database.command("ping")

                if pong["ok"] == 1:
                    return "Up"

                return "Down"
            except Exception as error:  # noqa: BLE001
                print(f"Error pinging database: {error}")
                return "Not reachable"
        return "Not Connected"

    @property
    def get_health_status(self) -> dict[str, dict[str, str | None] | str | float]:
        """get_health_status _summary_

        _extended_summary_

        :return: _description_
        :rtype: dict[str, dict[str, str | None] | str | float]
        """
        return {
            "version": self.API_VERSION,
            "service": "up",
            "environment": self.ENV,
            "cache": "NOT IMPLEMENTED",
            "cpu_usage": cpu_percent(interval=1),
            "memory_usage": virtual_memory().percent,
            "disk_usage": disk_usage("/").percent,
            "database": self.DB_TYPE,
        }

    @property
    def emails_maintainers_list(self) -> list[str]:
        """emails_maintainers_list _summary_

        _extended_summary_

        :return: _description_
        :rtype: list[str]
        """
        return str(self.MAINTAINERS_EMAILS).split(",")

    @property
    def get_api_prefix(self) -> str:
        """get_api_prefix _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return "/api/v1"

    @property
    def get_formatted_version(self) -> str:
        """get_formatted_version _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return f"v{self.API_VERSION}"

    @field_validator("API_VERSION", mode="before")
    @classmethod
    def parse_api_version(cls, value: str) -> str:
        """parse_api_version _summary_

        _extended_summary_

        :param value: _description_
        :type value: str
        :return: _description_
        :rtype: str
        """
        try:
            if value is None or value == "":
                return __version__
            return str(value)
        except ValueError as error:
            print("Error parsing API_VERSION: " + str(error))
            return value

    @field_validator("ALLOWED_CORS_ORIGIN", mode="before")
    @classmethod
    def parse_allowed_cors_origin(cls, unparsed_string: Tuple[str, list]) -> list[Literal["*"] | AnyHttpUrl]:
        """parse_allowed_cors_origin _summary_

        _extended_summary_

        :param unparsed_string: _description_
        :type unparsed_string: str
        :return: _description_
        :rtype: list[Literal["*"] | AnyHttpUrl]
        """
        if type(unparsed_string) == list:
            return unparsed_string
        try:
            if unparsed_string is None or unparsed_string in {"", "*"}:
                return ["*"]
            return str(unparsed_string).split(",")
        except ValueError as error:
            print("Error parsing ALLOWED_CORS_ORIGIN: " + str(error))
            return unparsed_string

    @field_validator("ALLOWED_METHODS", mode="before")
    @classmethod
    def parsed_allowed_methods(cls, value: str | list[str]) -> list[str]:
        """parsed_allowed_methods _summary_

        _extended_summary_

        :param value: _description_
        :type value: str | list[str]
        :return: _description_
        :rtype: list[str]
        """
        if isinstance(value, str):
            return [method.strip() for method in value.split(",")]
        return value

    @field_validator("ALLOWED_HEADERS", mode="before")
    @classmethod
    def parsed_allowed_headers(cls, value: str) -> list[str]:
        """parsed_allowed_headers _summary_

        _extended_summary_

        :param unparsed_string: _description_
        :type unparsed_string: str
        :return: _description_
        :rtype: list[str]
        """
        try:
            if isinstance(value, str):
                return [method.strip() for method in value.split(",")]
            return value
        except ValueError as error:
            print("Error parsing ALLOWED_HEADERS: " + str(error))
            return value


settings = Settings()
