# FILE: app/schemas.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True