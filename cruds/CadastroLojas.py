from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

# CRUD Lojas

def criar_loja(db: Session, loja: schemas.LojaCreate):
    # Cria uma nova loja
    db_loja = models.Loja(**loja.model_dump()) # Use .model_dump() para Pydantic v2+
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja)
    return db_loja

def listar_lojas(db: Session):
    # Lista todas as lojas
    return db.query(models.Loja).all()

def buscar_lojas(db: Session, loj_id: int):
    # Busca uma loja pelo ID
    return db.query(models.Loja).filter(models.Loja.id == loj_id).first()

def atualizar_lojas(db: Session, loj_id: int, novo: schemas.LojaCreate):
    # Atualiza uma loja existente
    loja = buscar_lojas(db, loj_id)
    if loja:
        for key, value in novo.model_dump(exclude_unset=True).items(): # Use .model_dump() para Pydantic v2+
            setattr(loja, key, value)
        db.commit()
        db.refresh(loja)
        return loja
    return None

def verificar_login_loja(db: Session, email: str, senha: str):
    # Verifica login da loja
    loja = db.query(models.Loja).filter(models.Loja.email == email, models.Loja.senha == senha).first()
    return loja

def deletar_loja(db: Session, loj_id: int):
    # Deleta uma loja
    loja = buscar_lojas(db, loj_id)
    if loja:
        db.delete(loja)
        db.commit()
        return loja
    return None