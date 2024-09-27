from sqlalchemy import String, text
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


def uuid_column():
    return mapped_column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        server_default=text("gen_random_uuid()"),
        default=uuid4
    )
def hex_color_column(nullable:bool = True):
    return mapped_column(
        String(7),
        nullable=nullable,
    )