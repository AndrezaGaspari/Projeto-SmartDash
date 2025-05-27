from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

# CRUD Lojas

def criar_loja(db: Session, loja: schemas.LojaCreate):
    db_loja = models.Loja(**loja.dict())
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja)
    return db_loja


def listar_lojas(db: Session):
    return db.query(models.Loja).all()

def buscar_lojas(db: Session, loj_id: int):
    return db.query(models.Loja).filter(models.Loja.id == loj_id).first()

def atualizar_lojas(db: Session, loj_id: int, novo: schemas.LojaCreate):
    loja = buscar_lojas(db, loj_id)
    if loja:
        for key, value in novo.dict().items():
            setattr(loja, key, value)
        db.commit()
        db.refresh(loja)
        return loja
    return None

def verificar_login_loja(db: Session, email: str, senha: str):
  
    loja = db.query(models.Loja).filter(models.Loja.email == email, models.Loja.senha == senha).first()
    return loja 

def deletar_loja(db: Session, loj_id: int):
    loja = buscar_lojas(db, loj_id)
    if loja:
        db.delete(loja)
        db.commit()
        return loja
    return None
