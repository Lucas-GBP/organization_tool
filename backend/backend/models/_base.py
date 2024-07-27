import re
from sqlalchemy import String, CheckConstraint, text
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

ts_vector_dict = 'portuguesedict'

class Base(DeclarativeBase):
    """
    Base class for sqlalchemy tables/models
    """
    @declared_attr
    def __tablename__(cls) -> str:
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return name

"""
Especific columns types
"""
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
"""
Checks
"""
def CheckColorHex(column_name:str, nullable:bool = True):
    checkName = "check_color_hex"
    if nullable:
        return CheckConstraint(
            f"({column_name} IS NULL OR {column_name}"+r" ~* '^#[a-f0-9]{6}$')",
            name=checkName
        )
    else:
        return CheckConstraint(
            "("+column_name+r" ~* '^#[a-f0-9]{6}$')",
            name=checkName
        )