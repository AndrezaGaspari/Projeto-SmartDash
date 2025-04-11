from pydantic import BaseModel
 
class ItemBase(BaseModel):

    nome: str

    descricao: str
 
class ItemCreate(ItemBase):

    pass
 
class Item(ItemBase):

    id: int
 
    class Config:

        from_attributes = True  # substitui orm_mode no Pydantic v2

 