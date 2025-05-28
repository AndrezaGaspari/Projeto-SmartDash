# seu schemas.py
from pydantic import BaseModel
from typing import List,Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field # Importe Field e EmailStr
from typing import Optional # Importe Optional se usar campos opcionais

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: Optional[date] = None # Opcional (se não tiver data de vencimento)
    quantidade: int # <--- ESTE CAMPO É OBRIGATÓRIO (se não tiver Optional ou = algum_valor)
    fabricacao:Optional[date] = None # Opcional (se não tiver data de fabricação)
    valor_produto: float # <--- ESTE CAMPO É OBRIGATÓRIO
    categoria: str
    fk_loja_id: int # <--- ESTE CAMPO É OBRIGATÓRIO

    # Adicione estes campos que vêm do frontend, se ainda não estiverem:
    imagem: Optional[str] = None
    disponivel: bool = True # Tornando disponivel com valor padrão no schema

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    class Config:
        from_attributes = True


class LojaBase(BaseModel):
    
    nome_fantasia: str
    razao_social: str
    cnpj: str 
    senha: str 
    estado: str
    cidade: str
    email: EmailStr
    cep: str                      # <--- NOVO CAMPO ADICIONADO (assumindo que é obrigatório)
    telefone: Optional[str] = None # <--- NOVO CAMPO ADICIONADO (assumindo que é opcional)


class LojaCreate(LojaBase):
    pass 

class Loja(LojaBase):
    id: int 
 
    class Config:
        from_attributes = True 

class LoginLoja(BaseModel):
    email: EmailStr
    senha: str

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

from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: Optional[date] = None
    quantidade: int
    fabricacao: Optional[date] = None
    valor_produto: float
    categoria: str
    fk_loja_id: int

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True



# Carrinho
from pydantic import BaseModel

class CarrinhoProdutoBase(BaseModel):
    produto_id: int
    revendedor_id: int
    quantidade: int
    nome_produto: str         
    preco_unitario: float    


class CarrinhoProdutoCreate(CarrinhoProdutoBase):
    pass


class CarrinhoProduto(CarrinhoProdutoBase):
    id: int

    class Config:
        from_attributes = True

