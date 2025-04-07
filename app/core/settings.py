from typing import Literal

from psutil import disk_usage, cpu_percent, virtual_memory
from pydantic import Field, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    ENV: str = Field("development")
    HOST: str = Field("0.0.0.0")  # noqa: S104
    PORT: int = Field(8087)
    DEBUG: bool = Field(False)  # noqa: FBT003
    ALLOWED_CORS_ORIGIN: str | list[Literal["*"] | AnyHttpUrl] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    MAINTAINERS_EMAILS: str = Field("luisangelmarcia@gmail.com")

    # Timeouts and intervals of delays
    DEFAULT_TIMEOUT: int = Field(300)
    SHORT_INTERVAL: int = Field(36)
    LONG_INTERVAL: int = Field(72)

    # Logger Settings
    LOGGER_LEVEL: str = Field("INFO")
    LOGGER_FORMAT: str = Field(
        "%(asctime)s - line:%(lineno)d - %(name)s - %(levelname)s - %(message)s",
    )
    LOGGER_FILE_NAME: str = Field("nuop-utils.log")

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
        return f"/api/{self.API_VERSION}"

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
    def parse_allowed_cors_origin(cls, unparsed_string: str) -> list[Literal["*"] | AnyHttpUrl]:
        """parse_allowed_cors_origin _summary_

        _extended_summary_

        :param unparsed_string: _description_
        :type unparsed_string: str
        :return: _description_
        :rtype: list[Literal["*"] | AnyHttpUrl]
        """
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

print(
    f"""
    Settings loaded:
    {settings.check_env_variables}
    """,
)
