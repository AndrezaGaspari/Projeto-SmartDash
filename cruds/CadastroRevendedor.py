from sqlalchemy.orm import Session
from banco_de_dados import models, schemas

# CRUD Revendedor
def criar_revendedor(db: Session, revendedor: schemas.RevendedorCreate):
    db_revendedor = models.Revendedor(**revendedor.dict())
    db.add(db_revendedor)
    db.commit()
    db.refresh(db_revendedor)
    return db_revendedor

def listar_revendedores(db: Session):
    return db.query(models.Revendedor).all()

def buscar_revendedor(db: Session, rev_id: int):
    return db.query(models.Revendedor).filter(models.Revendedor.id == rev_id).first()

def atualizar_revendedor(db: Session, rev_id: int, novo: schemas.RevendedorCreate):
    revendedor = buscar_revendedor(db, rev_id)
    if revendedor:
        for key, value in novo.dict().items():
            setattr(revendedor, key, value)
        db.commit()
        db.refresh(revendedor)
        return revendedor
    return None

def deletar_revendedor(db: Session, rev_id: int):
    revendedor = buscar_revendedor(db, rev_id)
    if revendedor:
        db.delete(revendedor)
        db.commit()
        return revendedor
    return None

import bcrypt

def verificar_login(db: Session, nome: str, senha: str):
    usuario = db.query(models.Revendedor).filter(models.Revendedor.nome == nome).first()

    if not usuario:
        return None

    if not bcrypt.checkpw(senha.encode('utf-8'), models.Revendedor.senha('utf-8')):
        return None

    return usuario
