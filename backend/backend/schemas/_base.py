from typing import TypeVar
from pydantic import BaseModel, ConfigDict


Model = TypeVar('Model', bound='BaseModel')


class BaseRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)