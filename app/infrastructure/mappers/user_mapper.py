from app.core.security import get_password
from app.domain.entities.user import User
from app.schemas.pydantic.user_schemas import UserCreate
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


def to_entity_user_from_beanie_user(doc: BeanieUser) -> User:
    return User(
        id=doc.id,
        email=doc.email,
        username=doc.username,
        first_name=doc.first_name,
        last_name=doc.last_name,
        hashed_password=doc.hashed_password,
        is_active=doc.is_active,
    )


def to_beanie_user_from_entity_user(entity: User) -> BeanieUser:
    try:
        return BeanieUser(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
        )
    except Exception as e:
        msg = "Failed to convert User to BeanieUser: " + str(e)
        raise ValueError(msg) from e


def to_entity_user_from_schema_create_user(create_schema: UserCreate) -> User:
    return User(
        email=create_schema.email,
        username=create_schema.username,
        first_name=create_schema.first_name,
        last_name=create_schema.last_name,
        hashed_password=get_password(create_schema.password),
    )
