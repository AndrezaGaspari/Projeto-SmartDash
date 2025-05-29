from sqlalchemy.orm import Session, joinedload
from banco_de_dados import models, schemas

def adicionar_Produto_carrinho(db: Session, item: schemas.CarrinhoProdutoCreate):
    # Adiciona ou atualiza a quantidade de um produto no carrinho
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.fk_produto_id == item.fk_produto_id,
        models.CarrinhoProduto.fk_revendedor_id == item.fk_revendedor_id
    ).first()

    if db_item:
        db_item.quantidade += item.quantidade
    else:
        db_item = models.CarrinhoProduto(
            fk_produto_id=item.fk_produto_id,
            fk_revendedor_id=item.fk_revendedor_id,
            quantidade=item.quantidade
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item

def listar_Produto_carrinho(db: Session, revendedor_id: int):
    # Lista todos os itens do carrinho de um revendedor, incluindo detalhes do produto
    return db.query(models.CarrinhoProduto).options(joinedload(models.CarrinhoProduto.produto)).filter(
        models.CarrinhoProduto.fk_revendedor_id == revendedor_id
    ).all()

def remover_Produto_carrinho(db: Session, revendedor_id: int, produto_id: int):
    # Remove um produto específico do carrinho de um revendedor
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.fk_revendedor_id == revendedor_id,
        models.CarrinhoProduto.fk_produto_id == produto_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def limpar_carrinho(db: Session, revendedor_id: int):
    # Limpa todos os itens do carrinho de um revendedor
    itens = db.query(models.CarrinhoProduto).filter(models.CarrinhoProduto.fk_revendedor_id == revendedor_id).all()

    for item in itens: # Itera e deleta cada item
        db.delete(item)
    db.commit()