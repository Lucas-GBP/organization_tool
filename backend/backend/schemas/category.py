from uuid import UUID

from ._base import BaseRecord, BaseModel
from .sub_category import SubCategoryIntegratedPost, SubCategory
from .utils import ColorField

class Category(BaseModel):
    uuid:UUID
    color:str|None = ColorField()
    sub_categories:list[SubCategory]|None = None
    title:str
    description:str|None

class CategoryRecord(BaseRecord):
    id:int
    uuid:UUID
    user_id:int

    title:str
    color:str|None = ColorField()
    description:str|None

    def to_base_model(self) -> Category:
        dumpin = self.model_dump()
        return Category(**dumpin)

class CategoryPost(BaseModel):
    user_uuid:UUID
    color:str|None = ColorField()
    sub_categories:list[SubCategoryIntegratedPost]|None = None
    title:str
    description:str|None = None

class CategoryPatch(BaseModel):
    uuid:UUID
    color:str|None = ColorField()
    title:str|None
    description:str|None