from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Produto, Base

app = FastAPI()

# Cria as tabelas no banco se não existirem
Base.metadata.create_all(bind=engine)

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema Pydantic
class ProdutoSchema(BaseModel):
    nome: str
    preco: float

    class Config:
        orm_mode = True

# POST - Criar produto
@app.post("/produtos")
def criar_produto(produto: ProdutoSchema, db: Session = Depends(get_db)):
    db_produto = Produto(nome=produto.nome, preco=produto.preco)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# GET - Listar produtos
@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()
