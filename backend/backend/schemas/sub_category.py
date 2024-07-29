from ._base import BaseRecord, BaseModel
from uuid import UUID

class SubCategory(BaseModel):
    uuid:UUID
    title:str
    color:str

class SubCategoryRecord(BaseRecord):
    id:int
    uuid:UUID
    category_id:int
    color:str

    title:str    
    def to_base_model(self) -> SubCategory:
        dumpin = self.model_dump()
        return SubCategory(**dumpin)

class SubCategoryIntegratedPost(BaseModel):
    title:str
    color:str

class SubCategoryPost(SubCategoryIntegratedPost):
    category_uuid:UUID

class SubCategoryPatch(BaseModel):
    uuid: UUID
    title: str|None
    color: str|None