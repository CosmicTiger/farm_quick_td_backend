from enum import Enum
from typing import Generic, TypeVar
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict, AliasGenerator, ValidationError
from pydantic.alias_generators import to_camel

from app.core.logger import logger
from app.utils.enums.sort_enum import SortOptions
from app.utils.enums.filter_capabilities_enum import FilterOperatorsNumberEnum, FilterLogicalOperatorsEnum
from app.utils.enums.datasource_filter_transformer_enum import DatasourceFilterTransformerEnum

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


class SortCapabilities(BaseModel):
    """SortCapabilities _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    field: str = Field(..., title="Field", description="Field to sort by")
    order: SortOptions = Field(..., title="Order", description="Order to sort by (asc/desc)")

    def build_sort_format(
        self,
        configure_to_datasource: DatasourceFilterTransformerEnum = DatasourceFilterTransformerEnum.default,
    ) -> str | None:
        """build_sorts_format _summary_

        _extended_summary_

        :return: _description_
        :rtype: list[str]
        """
        if self.sorts and (
            configure_to_datasource
            in (DatasourceFilterTransformerEnum.mongo_db, DatasourceFilterTransformerEnum.default)
        ):
            return f"{self.order.value}{self.field}"
        return None


FilterTypeValue = TypeVar("FilterTypeValue")
OperatorType = TypeVar("OperatorType", bound=Enum)

MultiFilterTypeValue = TypeVar("MultiFilterTypeValue", bound=FilterTypeValue | list[FilterTypeValue] | None)


class ValueDescriptionToFilter(BaseModel, Generic[MultiFilterTypeValue, OperatorType]):
    """ValueDescriptionToFilter _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    :param Generic: _description_
    :type Generic: _type_
    """

    value: MultiFilterTypeValue = Field(
        ...,
        title="Default value",
        description="Value that works as default filter value for the field which the filter would be applied to",
    )
    operator: OperatorType = Field(
        default_factory=FilterOperatorsNumberEnum.no_op,
        title="Operator",
        description="Operator to use for filtering",
    )


ValueDescriptionToFilterSchema = TypeVar("ValueDescriptionToFilterSchema", bound=ValueDescriptionToFilter)


class FilterCapabilities(
    BaseModel,
    Generic[ValueDescriptionToFilterSchema],
):
    """FilterCapabilities _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    fields: ValueDescriptionToFilterSchema = Field(
        ...,
        title="Fields",
        description="Fields to filter by",
    )
    logical_operator: FilterLogicalOperatorsEnum = Field(
        default_factory=FilterLogicalOperatorsEnum.no_op,
        title="Logical Operator",
        description="Logical operator to use for filtering",
    )


FilterSchema = TypeVar("FilterSchema", bound=FilterCapabilities)


class PaginationOptions(BaseModel, Generic[FilterSchema]):
    """PaginationCommonRequests _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    filters: FilterSchema | None = Field(
        default=None,
        title="Filters",
        description="Filters to apply to the request",
    )
    sorts: list[SortCapabilities] | None = Field(
        default=None,
        title="Sorts",
        description="Sorts to apply to the request",
    )

    def build_sorts_options(
        self,
        configure_to_datasource: DatasourceFilterTransformerEnum = DatasourceFilterTransformerEnum.default,
    ) -> list[str]:
        """build_sorts_options _summary_

        _extended_summary_

        :return: _description_
        :rtype: list[str]
        """
        if self.sorts and (
            configure_to_datasource
            in (DatasourceFilterTransformerEnum.mongo_db, DatasourceFilterTransformerEnum.default)
        ):
            return [sort.build_sort_format(configure_to_datasource) for sort in self.sorts]
        return []
