from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Tabela de associação entre Pedido e Produto (Relacionamento N:N)
relacionamento_pedido_produto = Table(
    "relacionamento_3",
    Base.metadata,
    Column("fk_pedido_id", Integer, ForeignKey("pedido.id")),
    Column("fk_produto_id", Integer, ForeignKey("produto.id"))
)

class Loja(Base):
    __tablename__ = "loja"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    estado = Column(String)
    cidade = Column(String)
    cnpj = Column(String)
    senha = Column(String)

    produtos = relationship("Produto", back_populates="loja")
    revendedores = relationship("Revendedor", back_populates="loja")

class Produto(Base):
    __tablename__ = "produto"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    vencimento = Column(Date)
    quantidade = Column(Integer)
    fabricacao = Column(Date)
    valor_produto = Column(Float)
    categoria = Column(String)
    fk_loja_id = Column(Integer, ForeignKey("loja.id"))

    loja = relationship("Loja", back_populates="produtos")
    pedidos = relationship("Pedido", secondary=relacionamento_pedido_produto, back_populates="produtos")



class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    valor_produto = Column(Float)
    categoria = Column(String)
    fk_loja_id = Column(Integer, ForeignKey("loja.id"))

class Revendedor(Base):
    __tablename__ = "revendedor"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cidade = Column(String)
    estado = Column(String)
    email = Column(String)
    senha = Column(String)
    cpf = Column(String)
    telefone = Column(String)
    data_nascimento = Column(Date)
    cep = Column(String)
    rua = Column(String)
    numero_casa = Column(Integer)
    complemento = Column(String)
    bairro = Column(String)
    fk_loja_id = Column(Integer, ForeignKey("loja.id"))

    loja = relationship("Loja", back_populates="revendedores")
    pedidos = relationship("Pedido", back_populates="revendedor")

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer, primary_key=True, index=True)
    valor_pedido = Column(Float)
    quantidade = Column(Integer)
    data_pedido = Column(Date)
    status = Column(Boolean)
    fk_revendedor_id = Column(Integer, ForeignKey("revendedor.id"))

    revendedor = relationship("Revendedor", back_populates="pedidos")
    produtos = relationship("Produto", secondary=relacionamento_pedido_produto, back_populates="pedidos")
    
