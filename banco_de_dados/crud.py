from sqlalchemy.orm import Session

from . import models, schemas
 
def criar_item(db: Session, item: schemas.ItemCreate):

    db_item = models.ItemDB(**item.dict())

    db.add(db_item)

    db.commit()

    db.refresh(db_item)

    return db_item
 
def listar_itens(db: Session):

    return db.query(models.ItemDB).all()
 
def atualizar_item(db: Session, item_id: int, novo_item: schemas.ItemCreate):

    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()

    if item:

        item.nome = novo_item.nome

        item.descricao = novo_item.descricao

        db.commit()

        db.refresh(item)

        return item

    return None
 
def deletar_item(db: Session, item_id: int):

    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()

    if item:

        db.delete(item)

        db.commit()

        return item

    return None
 