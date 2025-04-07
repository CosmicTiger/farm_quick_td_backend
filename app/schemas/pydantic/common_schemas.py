from typing import Generic, TypeVar
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict, AliasGenerator, ValidationError
from pydantic.alias_generators import to_camel

from app.core.logger import logger

M = TypeVar("M", bound=BaseModel)


class CommonResponse(BaseModel, Generic[M]):
    """CommonResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    message: str
    result: M | None


class CommonResponseOnlyResult(BaseModel, Generic[M]):
    """CommonResponseOnlyResult _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    result: M | None


class CommonSucessRequestResponse(BaseModel, Generic[M]):
    """_summary_

    _extended_summary_
    """

    message: str
    data: M | None


class CommonListResponse(BaseModel, Generic[M]):
    """CommonListResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    total: int | None
    data: list[M]


class CommonDeleteResponse(BaseModel, Generic[M]):
    """CommonDeleteResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    message: str
    deleted_entity: M


class CommonErrorResponse(BaseModel):
    """CommonErrorResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    message: str


class CommonHandledErrorResponse(BaseModel, Generic[M]):
    """CommonHandledErrorResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    message: str
    error: M


class TimeStamp(BaseModel):
    """TimeStampResponse _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    created_at: datetime | None = Field(..., title="createdAt")
    updated_at: datetime | None = Field(..., title="createdAt")

    model_config: ConfigDict = ConfigDict(
        populate_by_alias=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
    )

    def __init__(self, **data: dict) -> None:
        """__init__ _summary_

        _extended_summary_
        """
        try:
            super().__init__(**data)
        except ValidationError as error:
            logger.error(f"Validation Error: {error}")
            raise
