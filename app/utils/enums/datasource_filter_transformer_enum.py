from enum import Enum


class DatasourceFilterTransformerEnum(Enum):
    """DatasourceFilterTransformerEnum _summary_

    _extended_summary_

    :param Enum: _description_
    :type Enum: _type_
    """

    default = "default"
    mongo_db = "mongo_db"
    sqlite = "sqlite"
