from sqlalchemy.orm import Session
from banco_de_dados import models, schemas
import bcrypt

# CRUD Revendedor

def criar_revendedor(db: Session, revendedor: schemas.RevendedorCreate):
    # Cria um novo revendedor com senha hashed
    revendedor_data = revendedor.model_dump() # Use .model_dump() para Pydantic v2+

    # Hasheia a senha antes de salvar
    hashed_password_bytes = bcrypt.hashpw(revendedor_data["senha"].encode('utf-8'), bcrypt.gensalt(rounds=12))
    revendedor_data["senha"] = hashed_password_bytes.decode('utf-8')

    db_revendedor = models.Revendedor(**revendedor_data)
    db.add(db_revendedor)
    db.commit()
    db.refresh(db_revendedor)
    return db_revendedor

def listar_revendedores(db: Session):
    # Lista todos os revendedores
    return db.query(models.Revendedor).all()

def buscar_revendedor(db: Session, rev_id: int):
    # Busca um revendedor pelo ID
    return db.query(models.Revendedor).filter(models.Revendedor.id == rev_id).first()

def atualizar_revendedor(db: Session, rev_id: int, novo: schemas.RevendedorCreate):
    # Atualiza um revendedor existente
    revendedor = buscar_revendedor(db, rev_id)
    if revendedor:
        for key, value in novo.model_dump(exclude_unset=True).items(): # Use .model_dump() para Pydantic v2+
            # Não atualize a senha diretamente aqui sem hashear novamente se ela vier no 'novo'
            # Isso requer um tratamento mais específico se a senha puder ser atualizada por essa rota
            setattr(revendedor, key, value)
        db.commit()
        db.refresh(revendedor)
        return revendedor
    return None

def deletar_revendedor(db: Session, rev_id: int):
    # Deleta um revendedor
    revendedor = buscar_revendedor(db, rev_id)
    if revendedor:
        db.delete(revendedor)
        db.commit()
        return revendedor
    return None

def verificar_login(db: Session, email: str, senha: str):
    # Verifica o login do revendedor
    usuario = db.query(models.Revendedor).filter(models.Revendedor.email == email).first()
    if not usuario:
        return None
    # Compara a senha fornecida com a senha hashed no banco de dados
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        return None
    return usuario