from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

def adicionar_Produto_carrinho(db: Session, item: schemas.CarrinhoProdutoCreate):
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.fk_produto_id == item.fk_produto_id,   # <--- CORRIGIDO
        models.CarrinhoProduto.fk_revendedor_id == item.fk_revendedor_id # <--- CORRIGIDO
    ).first()

    if db_item:
        db_item.quantidade += item.quantidade
    else:
        db_item = models.CarrinhoProduto(
            fk_produto_id=item.fk_produto_id,    # <--- CORRIGIDO
            fk_revendedor_id=item.fk_revendedor_id, # <--- CORRIGIDO
            quantidade=item.quantidade
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item

# Listar itens do models.carrinho por revendedor
def listar_Produto_carrinho(db: Session, revendedor_id: int):
    # Esta função parece estar ok, já que o parâmetro `revendedor_id` é o que vem da URL
    return db.query(models.CarrinhoProduto).filter(models.CarrinhoProduto.fk_revendedor_id == revendedor_id).all() # Adicione .all() para retornar todos os resultados


def remover_Produto_carrinho(db: Session, revendedor_id: int, produto_id: int):
    db_item = db.query(models.CarrinhoProduto).filter(
        models.CarrinhoProduto.fk_revendedor_id == revendedor_id, # <--- CORRIGIDO
        models.CarrinhoProduto.fk_produto_id == produto_id        # <--- CORRIGIDO
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# Limpar models.carrinho todo de um revendedor
def limpar_carrinho(db: Session, revendedor_id: int):
    itens = db.query(models.CarrinhoProduto).filter(models.CarrinhoProduto.fk_revendedor_id == revendedor_id).all() # Adicione .all() para buscar os itens

    for Produto in itens: # Loop pelos itens para deletar
        db.delete(Produto)
    db.commit()
