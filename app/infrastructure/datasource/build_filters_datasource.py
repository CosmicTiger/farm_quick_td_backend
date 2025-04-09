from beanie.operators import NE, GTE, LTE, Eq, In, Or, And, Nor, Not, NotIn

from app.schemas.pydantic.task_schemas import ValueDescriptionToFilter
from app.schemas.pydantic.common_schemas import FilterCapabilities

OPERATOR_MAPPING = {
    "eq": lambda f, v: Eq(f, v),
    "ne": lambda f, v: NE(f, v),
    "gte": lambda f, v: GTE(f, v),
    "lte": lambda f, v: LTE(f, v),
    "in": lambda f, v: In(f, v),
    "not_in": lambda f, v: NotIn(f, v),
}

LOGICAL_OPERATOR_MAPPING = {
    "and": lambda *args: And(*args),
    "or": lambda *args: Or(*args),
    "not": lambda *args: Not(*args),
    "nor": lambda *args: Nor(*args),
    "no_op": lambda *args: And(*args),
    "": lambda *args: And(*args),
}


def build_beanie_filter(filters: FilterCapabilities) -> any:
    """build_beanie_filter _summary_

    _extended_summary_

    :param filters: _description_
    :type filters: FilterCapabilities
    :raises ValueError: _description_
    :raises ValueError: _description_
    :raises ValueError: _description_
    :raises ValueError: _description_
    :return: _description_
    :rtype: _type_
    """
    expressions = []

    if not filters.fields:
        raise ValueError("No filters provided to build the query.")

    fields_to_filter_dumped = filters.fields.model_dump(exclude_unset=True)

    for field, _filter in fields_to_filter_dumped.items():
        parsed_filter = ValueDescriptionToFilter(**_filter)

        if parsed_filter.operator == "no_op":
            msg = f"Operator is required for field {field}, field will be ignored"
            raise ValueError(msg)

        if parsed_filter.value is None and parsed_filter.operator != "no_op":
            msg = f"Value is required for field {field}, field will be ignored"
            raise ValueError(msg)

        if parsed_filter.operator not in OPERATOR_MAPPING:
            msg = f"Unsupported operator: {parsed_filter.operator}"
            raise ValueError(msg)

        expression = OPERATOR_MAPPING[parsed_filter.operator](field, parsed_filter.value)
        expressions.append(expression)

    return {
        "expression": expressions,
        "logical_operator": filters.logical_operator.value,
    }
