from ._base import BaseRecord, BaseModel
from uuid import UUID
from .utils import ColorField

"""
    HTTP Operations
"""
class SubCategoryIntegratedPost(BaseModel):
    """
        Schema usado para quando você POST uma Category, 
        junto com uma subCategory
    """
    title:str
    color:str = ColorField()

class SubCategoryPost(SubCategoryIntegratedPost):
    category_uuid:UUID

class SubCategoryPatch(BaseModel):
    uuid: UUID
    title: str|None
    color: str|None  = ColorField()

"""
    Database Operations
"""
class SubCategory(BaseModel):
    uuid:UUID
    title:str
    color:str = ColorField()
class SubCategoryCreate(SubCategoryPost):
    category_uuid:UUID
    title:str
    color:str = ColorField()
class SubCategoryUpdate(SubCategoryPatch):
    title: str|None
    color: str|None  = ColorField()

"""
    Database Objects
"""
class SubCategoryTable(BaseRecord):
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