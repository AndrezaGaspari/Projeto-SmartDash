from sqlalchemy.orm import Session # Isso é para o type hint (db: Session)
from banco_de_dados import models, schemas # Certifique-se que estas estão corretas

# CRUD Produto

# No seu cruds/CadastroProdutos.py (APÓS RENOMEAR A COLUNA NO models.py)

def criar_produto(db: Session, produto: schemas.ProdutoCreate):
    # Isso agora vai funcionar, pois 'valor_produto' existirá no models.Produto
    # e 'disponivel' e 'imagem' também serão incluídos se estiverem no schema.
    db_produto = models.Produto(**produto.model_dump()) # Use .model_dump() para Pydantic v2+
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def atualizar_produto(db: Session, prod_id: int, novo: schemas.ProdutoCreate):
    produto_db = buscar_produto(db, prod_id) # Renomeado para evitar conflito com 'produto' no loop
    if produto_db:
        # Isso agora vai funcionar, pois 'valor_produto', 'disponivel', 'imagem'
        # e outros campos do schema serão mapeados corretamente.
        for key, value in novo.model_dump(exclude_unset=True).items(): # exclude_unset para atualizar apenas campos enviados
            setattr(produto_db, key, value)
        db.commit()
        db.refresh(produto_db)
        return produto_db
    return None

def buscar_produto(db: Session, prod_id: int):
    return db.query(models.Produto).filter(models.Produto.id == prod_id).first()

def listar_produtos(db: Session):
    return db.query(models.Produto).all()


def deletar_produto(db: Session, prod_id: int):
    produto = buscar_produto(db, prod_id)
    if produto:
        db.delete(produto)
        db.commit()
        return produto
    return None