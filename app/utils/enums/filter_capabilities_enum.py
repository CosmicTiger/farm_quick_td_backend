from enum import Enum
from typing import TypeVar

T = TypeVar("T")


class FilterOperatorsStringAndBooleanEnum(str, Enum):
    """FilterOperatorsCompactEnum _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    no_op = ""
    eq = "eq"
    contains = "in"
    not_contains = "not_in"
    ne = "ne"


class FilterOperatorsNumberEnum(str, Enum):
    """FilterOperatorsTotalEnum _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    no_op = ""
    eq = "eq"
    gt = "gt"
    gte = "gte"
    contains = "in"
    not_contains = "not_in"
    lt = "lt"
    lte = "lte"
    ne = "ne"


class FilterOperatorsDateEnum(str, Enum):
    """FilterOperatorsDateEnum _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    no_op = ""
    eq = "eq"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    ne = "ne"


class FilterLogicalOperatorsEnum(str, Enum):
    """FilterLogicalOperatorsEnum _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    no_op = ""
    and_ = "and"
    or_ = "or"
    nor = "nor"
    not_ = "not"
