from sqlalchemy.orm import Session
from banco_de_dados import models, schemas
import bcrypt
# CRUD Revendedor
def criar_revendedor(db: Session, revendedor: schemas.RevendedorCreate):
    # Crie um dicionário mutável a partir dos dados do revendedor
    revendedor_data = revendedor.dict()

    # Hashear a senha antes de criar o objeto do modelo
    # Gera um salt (parte aleatória para o hash) e hasheia a senha
    hashed_password_bytes = bcrypt.hashpw(revendedor_data["senha"].encode('utf-8'), bcrypt.gensalt(rounds=12))
    # Decodifica o hash de bytes para string para salvar no banco de dados
    revendedor_data["senha"] = hashed_password_bytes.decode('utf-8')

    # Cria o objeto do modelo Revendedor com a senha hashed
    db_revendedor = models.Revendedor(**revendedor_data)

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

def verificar_login(db: Session, email: str, senha: str):
    usuario = db.query(models.Revendedor).filter(models.Revendedor.email == email).first()
    if not usuario:
        return None
    # Verifique a senha
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        return None
    return usuario