from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

# CRUD Produto

def criar_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def listar_produtos(db: Session):
    return db.query(models.Produto).all()

def buscar_produto(db: Session, prod_id: int):
    return db.query(models.Produto).filter(models.Produto.id == prod_id).first()

def atualizar_produto(db: Session, prod_id: int, novo: schemas.ProdutoCreate):
    produto = buscar_produto(db, prod_id)
    if produto:
        for key, value in novo.dict().items():
            setattr(produto, key, value)
        db.commit()
        db.refresh(produto)
        return produto
    return None

def deletar_produto(db: Session, prod_id: int):
    produto = buscar_produto(db, prod_id)
    if produto:
        db.delete(produto)
        db.commit()
        return produto
    return None