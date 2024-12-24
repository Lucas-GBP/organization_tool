from .utils.base import BaseRecord, BaseModel
from uuid import UUID


"""
    HTTP Operations
"""
class UserGet(BaseModel):
    uuid:UUID
    nickname:str
class UserPost(BaseModel):
    nickname:str
    password: str
class UserPatch(BaseModel):
    nickname:str|None

"""
    Database Operations
"""
class User(UserGet):
    ...
class UserCreate(BaseModel):
    nickname:str
    hashed_password:str
class UserUpdate(UserPatch):
    ...

"""
    Database Objects
"""
class UserTable(BaseRecord):
    id:int
    uuid:UUID
    nickname:str
    hashed_password:str

    def to_base_model(self) -> User:
        return User(
            nickname=self.nickname,
            uuid=self.uuid
        )
