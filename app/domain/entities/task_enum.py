from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum."""

    DRAFT = 0
    BACKLOG = 1
    TODO = 2
    IN_PROGRESS = 3
    BLOCKER = 4
    DONE = 5
    CANCELLED = 6
    DUPLICATE = 7


class Priority(str, Enum):
    """Priority _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    NO_PRIORITY = 0
    URGENT = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class SubTaskRelationType(str, Enum):
    """SubTaskRelationType _summary_

    _extended_summary_

    :param str: _description_
    :type str: _type_
    :param Enum: _description_
    :type Enum: _type_
    """

    BLOCKS = "blocks"
    DEPENDS_ON = "depends_on"
    RELATES_TO = "relates_to"
    DUPLICATE = "duplicate"
