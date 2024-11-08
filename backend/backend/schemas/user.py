from ._base import BaseRecord, BaseModel
from uuid import UUID


"""
    HTTP Operations
"""
class UserGet(BaseModel):
    uuid:UUID
    name:str
class UserPost(BaseModel):
    name:str
class UserPatch(BaseModel):
    name:str|None

"""
    Database Operations
"""
class User(UserGet):
    ...
class UserCreate(UserPost):
    ...
class UserUpdate(UserPatch):
    ...

"""
    Database Objects
"""
class UserTable(BaseRecord):
    id:int
    uuid:UUID
    name:str

    def to_base_model(self) -> User:
        return User(
            name=self.name,
            uuid=self.uuid
        )
