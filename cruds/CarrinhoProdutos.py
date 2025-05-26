from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

def adicionar_Produto_carrinho(db: Session, item: schemas.CarrinhoProdutoCreate):
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.produto_id == item.produto_id,
        models.CarrinhoProduto.revendedor_id == item.revendedor_id
    ).first()

    if db_item:
        db_item.quantidade += item.quantidade
    else:
        db_item = models.CarrinhoProduto(
            produto_id=item.produto_id,
            revendedor_id=item.revendedor_id,
            quantidade=item.quantidade
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item


# Listar itens do models.carrinho por revendedor
def listar_Produto_carrinho(db: Session, revendedor_id: int):
    return db.query(models.CarrinhoProduto).filter(models.CarrinhoProduto.revendedor_id == revendedor_id)



def remover_Produto_carrinho(db: Session, revendedor_id: int, produto_id: int):
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.revendedor_id == revendedor_id,
        models.CarrinhoProduto.produto_id == produto_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# Limpar models.carrinho todo de um revendedor
def limpar_carrinho(db: Session, revendedor_id: int):
    itens = db.query(models.CarrinhoProduto).filter(models.CarrinhoProduto.revendedor_id == revendedor_id)

    for Produto in itens:
        db.delete(Produto)
    db.commit()
