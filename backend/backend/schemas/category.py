from uuid import UUID

from ._base import BaseRecord, BaseModel
from .sub_category import SubCategoryIntegratedPost, SubCategory, SubCategoryTable
from .utils import ColorField

"""
    HTTP Operations
"""
class CategoryPost(BaseModel):
    user_uuid:UUID
    color:str|None = ColorField()
    title:str
    description:str|None = None

class CategoryWithSubCategoryPost(CategoryPost):
    sub_categories:list[SubCategoryIntegratedPost]|None = None

class CategoryPatch(BaseModel):
    uuid:UUID
    color:str|None = ColorField()
    title:str|None
    description:str|None

"""
    Database Operations
"""
class Category(BaseModel):
    uuid:UUID
    color:str|None = ColorField()
    title:str
    description:str|None

class CategoryWithSubCategory(Category):
    sub_categories:list[SubCategory]|None = None
class CategoryCreate(CategoryPost):
    color:str|None = ColorField()
    title:str
    description:str|None = None
class CategoryUpdate(BaseModel):
    color:str|None = ColorField()
    title:str|None
    description:str|None

"""
    Database Objects
"""
class CategoryTable(BaseRecord):
    id:int
    uuid:UUID
    user_id:int

    title:str
    color:str|None = ColorField()
    description:str|None

    def to_base_model(self) -> Category:
        return Category(
            uuid=self.uuid,
            color=self.color,
            title=self.title,
            description=self.description
        )

"""
    Multiples db Objects Composed
"""
class CategoryWithSubCategoryComposed(CategoryTable):
    sub_categories:list[SubCategoryTable]|None = None

    def to_base_model(self) -> CategoryWithSubCategory:
        sub_categories_list:list[SubCategory]|None = None
        if self.sub_categories is not None:
            sub_categories_list = []
            for item in self.sub_categories:
                sub_categories_list.append(item.to_base_model())

        return CategoryWithSubCategory(
            uuid=self.uuid,
            color=self.color,
            title=self.title,
            description=self.description,
            sub_categories=sub_categories_list
        )