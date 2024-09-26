from ._base import BaseRecord, BaseModel
from uuid import UUID
from .utils import ColorField

class SubCategory(BaseModel):
    uuid:UUID
    title:str
    color:str = ColorField()

class SubCategoryRecord(BaseRecord):
    id:int
    uuid:UUID
    category_id:int
    color:str = ColorField()

    title:str    
    def to_base_model(self):
        return SubCategory(
            uuid=self.uuid,
            title=self.title,
            color=self.color
        )

class SubCategoryIntegratedPost(BaseModel):
    title:str
    color:str = ColorField()

class SubCategoryPost(SubCategoryIntegratedPost):
    category_uuid:UUID

class SubCategoryPatch(BaseModel):
    uuid: UUID
    title: str|None
    color: str|None  = ColorField()