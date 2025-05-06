from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Produto
from schemas import ProdutoSchema, ProdutoCreate
from typing import List

# Cria as tabelas no banco (caso ainda não existam)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência de sessão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET - Listar todos os produtos
@app.get("/produtos", response_model=List[ProdutoSchema])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()

# POST - Criar novo produto
@app.post("/produtos", response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        data_fabricacao=produto.data_fabricacao,
        data_validade=produto.data_validade,
        descricao=produto.descricao
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# PUT - Atualizar produto existente
@app.put("/produtos/{produto_id}", response_model=ProdutoSchema)
def atualizar_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db_produto.nome = produto.nome
    db_produto.preco = produto.preco
    db_produto.data_fabricacao = produto.data_fabricacao
    db_produto.data_validade = produto.data_validade
    db_produto.descricao = produto.descricao

    db.commit()
    db.refresh(db_produto)
    return db_produto

# DELETE - Remover produto
@app.delete("/produtos/{produto_id}", response_model=ProdutoSchema)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return db_produto
