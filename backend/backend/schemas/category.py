from ._base import BaseRecord, BaseModel
from uuid import UUID
from .sub_category import SubCategoryIntegratedPost, SubCategory

class Category(BaseModel):
    uuid:UUID
    color:str|None = None
    sub_categories:list[SubCategory]|None = None
    title:str
    description:str|None

class CategoryRecord(BaseRecord):
    id:int
    uuid:UUID
    user_id:int

    title:str
    color:str|None
    description:str|None

    def to_base_model(self) -> Category:
        dumpin = self.model_dump()
        return Category(**dumpin)

class CategoryPost(BaseModel):
    user_uuid:UUID
    color:str|None = None
    sub_categories:list[SubCategoryIntegratedPost]|None = None
    title:str
    description:str|None = None

class CategoryPatch(BaseModel):
    uuid:UUID
    color:str|None
    title:str|None
    description:str|None