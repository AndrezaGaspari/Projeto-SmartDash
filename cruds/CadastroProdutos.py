from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

# Funções CRUD de Produto

def criar_produto(db: Session, produto: schemas.ProdutoCreate):
    # Cria um novo produto
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def atualizar_produto(db: Session, prod_id: int, novos_dados: schemas.ProdutoCreate):
    # Atualiza um produto existente
    produto_no_db = buscar_produto(db, prod_id)
    if produto_no_db:
        for key, value in novos_dados.model_dump(exclude_unset=True).items():
            setattr(produto_no_db, key, value)
        db.commit()
        db.refresh(produto_no_db)
        return produto_no_db
    return None

def buscar_produto(db: Session, prod_id: int):
    # Busca um produto pelo ID
    return db.query(models.Produto).filter(models.Produto.id == prod_id).first()

def listar_produtos(db: Session):
    # Lista todos os produtos
    return db.query(models.Produto).all()

def deletar_produto(db: Session, prod_id: int):
    # Deleta um produto
    produto_para_deletar = buscar_produto(db, prod_id)
    if produto_para_deletar:
        db.delete(produto_para_deletar)
        db.commit()
        return produto_para_deletar
    return None