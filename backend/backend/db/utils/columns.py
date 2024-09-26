from uuid import uuid4, UUID as PyUUID
from sqlalchemy import Integer, String, text
from sqlalchemy.orm import mapped_column, MappedColumn
from sqlalchemy.dialects.postgresql import UUID

def primary_id_column() -> MappedColumn[int]:
    return mapped_column(Integer, primary_key=True)

def uuid_column(unique:bool = True, index:bool = True) -> MappedColumn[PyUUID]:
    return mapped_column(
        UUID(as_uuid=True),
        unique=unique,
        index=index,
        server_default=text("gen_random_uuid()"),
        default=uuid4
    )

def hex_color_column(nullable:bool = True):
    return mapped_column(
        String(7),
        nullable=nullable,
    )
