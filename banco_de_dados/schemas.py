from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: date
    quantidade: int
    fabricacao: date
    valor_produto: float
    categoria: str
    fk_loja_id: int

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

# Loja
class LojaBase(BaseModel):
    nome: str
    estado: str
    cidade: str
    cnpj: str
    senha: str  # Adicionado conforme modelo

class LojaCreate(LojaBase):
    pass

class Loja(LojaBase):
    id: int

    class Config:
        from_attributes = True

# Revendedor
class RevendedorBase(BaseModel):
    nome: str
    cidade: str
    estado: str
    email: str
    senha: str
    cpf: str
    telefone: str
    data_nascimento: date
    cep: str
    rua: str
    numero_casa: int
    complemento: Optional[str] = None
    bairro: str
    fk_loja_id: int

class RevendedorCreate(RevendedorBase):
    pass

class Revendedor(RevendedorBase):
    id: int

    class Config:
        from_attributes = True

# Pedido
class PedidoBase(BaseModel):
    valor_pedido: float
    quantidade: int
    data_pedido: date
    status: bool
    fk_revendedor_id: int
    produto_ids: List[int]  # Para relacionamento N:N

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int

    class Config:
        from_attributes = True
