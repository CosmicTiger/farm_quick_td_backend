from enum import Enum, IntEnum


class TaskStatus(IntEnum):
    """TaskStatus

    Enum to represent the current state of the Task:

    - 0: DRAFT - The task is in draft state in order to be edited later
    - 1: BACKLOG - The task is in the backlog and should be done later
    - 2: TODO - The task is in the TODO list and should be done
    - 3: IN_PROGRESS - The task is in progress and should be done
    - 4: BLOCKER - The task is blocked and should be done later
    - 5: DONE - The task is done and should be archived
    - 6: CANCELLED - The task is cancelled and should be archived
    - 7: DUPLICATE - The task is a duplicate of another task and should be archived
    """

    DRAFT = 0
    BACKLOG = 1
    TODO = 2
    IN_PROGRESS = 3
    BLOCKER = 4
    DONE = 5
    CANCELLED = 6
    DUPLICATE = 7


class Priority(IntEnum):
    """Priority

    Enum to represent the priority that the Task has:

    - 0: NO_PRIORITY - The task has no priority over the board
    - 1: URGENT - The task is urgent and should be done as soon as possible
    - 2: HIGH - The task is high priority and should be done as soon as possible
    - 3: MEDIUM - The task is medium priority and should be done as soon as possible
    - 4: LOW - The task is low priority and should be done as soon as possible
    """

    NO_PRIORITY = 0
    URGENT = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class SubTaskRelationType(str, Enum):
    """SubTaskRelationType

    Relation types for that the sub tasks listed in the task can have:

    - block: BLOCKS - The sub task blocks the main task
    - depends_on: DEPENDS_ON - The sub task depends on the main task
    - relates_to: RELATES_TO - The sub task relates to the main task
    - duplicate: DUPLICATE - The sub task is a duplicate of the main task
    """

    BLOCKS = "blocks"
    DEPENDS_ON = "depends_on"
    RELATES_TO = "relates_to"
    DUPLICATE = "duplicate"
