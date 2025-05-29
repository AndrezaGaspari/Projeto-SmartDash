# Seu schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# --- Schemas de Produto ---
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: Optional[date] = None
    quantidade: int
    fabricacao: Optional[date] = None
    valor_produto: float
    categoria: str
    fk_loja_id: int
    # **** CORREÇÃO/ADIÇÃO IMPORTANTE AQUI ****
    imagem: Optional[str] = None       # <--- Adicione este campo para a URL da imagem
    disponivel: bool = True            # <--- Adicione este campo com valor padrão
                                       # Se você não quiser que seja padrão True, remova "= True"
                                       # mas é bom ter um padrão para não esquecer de enviar.

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic v1.x

# --- Schemas de Loja ---
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

# --- Schemas de Revendedor ---
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

# --- Schemas de Pedido ---
class PedidoBase(BaseModel):
    valor_pedido: float
    quantidade: int
    data_pedido: date
    status: bool # Assumindo que 'status' é um booleano (ativo/inativo, finalizado/pendente)
    fk_revendedor_id: int
    # produto_ids: List[int] # <--- Isso é para N:N, que é mais complexo com o carrinho.
                              # Se o pedido for gerado A PARTIR do carrinho, você
                              # pode precisar de outro schema de entrada para o pedido
                              # que não inclua uma lista de IDs.
                              # Ou você terá um modelo de 'ItemPedido' que vincula pedido a produto.

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas de Carrinho ---
# **** CORREÇÃO IMPORTANTE AQUI ****
# Seus nomes de campo para o carrinho no schema não estão alinhados com o que
# o FastAPI espera para a rota de adicionar ao carrinho (que usa `item.fk_produto_id` e `item.fk_revendedor_id`).
# Além disso, nome_produto e preco_unitario devem vir do produto, não do item do carrinho diretamente.
class CarrinhoProdutoBase(BaseModel):
    fk_produto_id: int   # <--- Renomeado de 'produto_id' para 'fk_produto_id'
    fk_revendedor_id: int # <--- Renomeado de 'revendedor_id' para 'fk_revendedor_id'
    quantidade: int

# Seu schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# --- Schemas de Produto ---
class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    vencimento: Optional[date] = None
    quantidade: int
    fabricacao: Optional[date] = None
    valor_produto: float
    categoria: str
    fk_loja_id: int
    # **** CORREÇÃO/ADIÇÃO IMPORTANTE AQUI ****
    imagem: Optional[str] = None       # <--- Adicione este campo para a URL da imagem
    disponivel: bool = True            # <--- Adicione este campo com valor padrão
                                       # Se você não quiser que seja padrão True, remova "= True"
                                       # mas é bom ter um padrão para não esquecer de enviar.

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic v1.x

# --- Schemas de Loja ---
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

# --- Schemas de Revendedor ---
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

# --- Schemas de Pedido ---
class PedidoBase(BaseModel):
    valor_pedido: float
    quantidade: int
    data_pedido: date
    status: bool # Assumindo que 'status' é um booleano (ativo/inativo, finalizado/pendente)
    fk_revendedor_id: int
    # produto_ids: List[int] # <--- Isso é para N:N, que é mais complexo com o carrinho.
                              # Se o pedido for gerado A PARTIR do carrinho, você
                              # pode precisar de outro schema de entrada para o pedido
                              # que não inclua uma lista de IDs.
                              # Ou você terá um modelo de 'ItemPedido' que vincula pedido a produto.

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas de Carrinho ---
# **** CORREÇÃO IMPORTANTE AQUI ****
# Seus nomes de campo para o carrinho no schema não estão alinhados com o que
# o FastAPI espera para a rota de adicionar ao carrinho (que usa `item.fk_produto_id` e `item.fk_revendedor_id`).
# Além disso, nome_produto e preco_unitario devem vir do produto, não do item do carrinho diretamente.
class CarrinhoProdutoBase(BaseModel):
    fk_produto_id: int   # <--- Renomeado de 'produto_id' para 'fk_produto_id'
    fk_revendedor_id: int # <--- Renomeado de 'revendedor_id' para 'fk_revendedor_id'
    quantidade: int

class CarrinhoProdutoCreate(CarrinhoProdutoBase):
    pass

class CarrinhoProduto(CarrinhoProdutoBase):
    id: int
    # Opcional: Para retornar os detalhes do produto e o nome/preço no carrinho
    # Você precisaria de um relacionamento no models.py para que o ORM possa carregá-los
    # produto: Produto # Se o seu modelo CarrinhoProduto tem um relacionamento com Produto
    # nome_produto: str # Estes campos seriam populados dinamicamente no backend, não armazenados no carrinho
    # preco_unitario: float # Estes campos seriam populados dinamicamente no backend, não armazenados no carrinho

    class Config:
        from_attributes = True


        

        