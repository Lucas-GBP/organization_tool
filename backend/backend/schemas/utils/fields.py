from pydantic import Field
from typing import Any

def ColorField(default:Any = None, nullable:bool = True):
    return Field(
        max_length=7, 
        min_length=7, 
        pattern=r'#[0-9A-Fa-f]{6}', 
        default=default
    )