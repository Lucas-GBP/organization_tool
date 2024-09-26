from typing import Any
from pydantic import Field
from pydantic_core import PydanticUndefined

def ColorField(default:Any = PydanticUndefined):
    return Field(
        max_length=7, 
        min_length=7, 
        pattern=r'#[0-9A-Fa-f]{6}', 
        default=default
    )