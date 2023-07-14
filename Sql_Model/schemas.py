from pydantic import BaseModel

class ItemBase(BaseModel):
    id : int
    description : str | None = None

class ItemCreate(ItemBase):
    pass
