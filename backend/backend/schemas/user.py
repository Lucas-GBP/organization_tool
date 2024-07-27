from ._base import BaseRecord
from uuid import UUID

class UserRecord(BaseRecord):
    id:int
    uuid:UUID
    name:str