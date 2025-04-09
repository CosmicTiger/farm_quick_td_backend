from enum import Enum


class BeanieOperators(Enum):
    """BeanieOperators _summary_"""

    no_op = ""
    eq = "eq"
    gt = "gt"
    gte = "gte"
    contains = "in"
    not_contains = "not_in"
    lt = "lt"
    lte = "lte"
    ne = "ne"
