from app.core.logger import logger
from app.schemas.pydantic.task_schemas import TaskCreate, TaskCreateWithMetadata
from app.infrastructure.mappers.user_mapper import to_beanie_user_from_entity_user
from app.infrastructure.models.odm.beanie_task_model import BeanieTask
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


async def to_beanie_task_from_schema_task_create(create_schema: TaskCreate, created_by: BeanieUser) -> BeanieTask:
    """Convert TaskCreate schema to BeanieTask model.

    Args:
        create_schema (TaskCreate): The TaskCreate schema.
        created_by (BeanieUser): The user who created the task.

    Returns:
        BeanieTask: The BeanieTask model.
    """
    try:
        data_payload_processed = create_schema.model_dump(exclude_unset=True)
        data_payload_processed["created_by"] = created_by

        validated_subtasks = None
        if "sub_tasks" in data_payload_processed:
            try:
                validated_subtasks = await BeanieTask.validate_sub_tasks(data_payload_processed["sub_tasks"])
            except Exception as error:  # noqa: BLE001
                msg = (
                    "Subtasks validation failed: "
                    + str(error)
                    + " sub_tasks won't be created for the task by name "
                    + str(
                        data_payload_processed["title"],
                    )
                )
                logger.warning(msg)

        if "assigned_to" in data_payload_processed and data_payload_processed["assigned_to"] is not None:
            assigned_user = await BeanieUser.get(
                data_payload_processed["assigned_to"],
            )
            if not assigned_user:
                raise ValueError("Assigned user not found")  # noqa: TRY301
            data_payload_processed["assigned_to"] = assigned_user

        task_to_create = TaskCreateWithMetadata(
            **{
                **data_payload_processed,
                "sub_tasks": validated_subtasks,
                "created_by": to_beanie_user_from_entity_user(created_by),
            },
        )

        return BeanieTask(
            title=task_to_create.title,
            description=task_to_create.description,
            status=task_to_create.status,
            priority=task_to_create.priority,
            is_archived=task_to_create.is_archived,
            sub_tasks=task_to_create.sub_tasks,
            due_date=task_to_create.due_date,
            assigned_to=task_to_create.assigned_to,
            created_by=task_to_create.created_by,
            updated_by=task_to_create.updated_by,
        )
    except Exception as e:
        msg = "Failed to convert TaskCreate to BeanieTask: " + str(e)
        raise ValueError(msg) from e
