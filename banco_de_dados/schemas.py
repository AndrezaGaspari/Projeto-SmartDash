from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# Schemas de Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: Optional[date] = None
    quantidade: int
    fabricacao: Optional[date] = None
    valor_produto: float
    categoria: str
    fk_loja_id: int
    imagem: Optional[str] = None
    disponivel: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    class Config:
        from_attributes = True

class ProdutoNoCarrinho(BaseModel):
    # Schema leve para detalhes do produto no carrinho
    id: int
    nome: str
    valor_produto: float
    imagem: Optional[str] = None

    class Config:
        from_attributes = True

# Schemas de Loja
class LojaBase(BaseModel):
    nome_fantasia: str
    razao_social: str
    cnpj: str
    senha: str
    estado: str
    cidade: str
    email: EmailStr
    cep: str
    telefone: Optional[str] = None

class LojaCreate(LojaBase):
    pass

class Loja(LojaBase):
    id: int
    class Config:
        from_attributes = True

class LoginLoja(BaseModel):
    email: EmailStr
    senha: str

# Schemas de Revendedor
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

class LoginRevendedor(BaseModel):
    email: str
    senha: str

# Schemas de Pedido
class PedidoBase(BaseModel):
    valor_pedido: float
    quantidade: int
    data_pedido: date
    status: bool # Considerar mudar para str no futuro
    fk_revendedor_id: int

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    class Config:
        from_attributes = True

# Schemas de Carrinho
class CarrinhoProdutoBase(BaseModel):
    fk_produto_id: int
    fk_revendedor_id: int
    quantidade: int

class CarrinhoProdutoCreate(CarrinhoProdutoBase):
    pass

class CarrinhoProduto(CarrinhoProdutoBase):
    id: int
    class Config:
        from_attributes = True

class CarrinhoProdutoDisplay(BaseModel):
    # Schema de saída para itens do carrinho com detalhes do produto
    id: int
    fk_produto_id: int
    fk_revendedor_id: int
    quantidade: int
    produto: ProdutoNoCarrinho # Objeto ProdutoNoCarrinho aninhado

    class Config:
        from_attributes = True