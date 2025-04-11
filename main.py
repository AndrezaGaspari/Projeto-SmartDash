from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from banco_de_dados.database import Engine, Base, SessionLocal

from banco_de_dados import crud, schemas
 
# Criação das tabelas

Base.metadata.create_all(bind=Engine)
 
app = FastAPI()
 
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
 
@app.get("/items", response_model=list[schemas.Item])

def pegar(db: Session = Depends(get_db)):

    return crud.listar_itens(db)
 
@app.post("/items", response_model=schemas.Item)

def criar_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):

    return crud.criar_item(db=db, item=item)
 
@app.put("/items/{item_id}", response_model=schemas.Item)

def atualizar(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):

    atualizado = crud.atualizar_item(db, item_id, item)

    if atualizado:

        return atualizado

    return {"erro": "Item não encontrado"}
 
@app.delete("/items/{item_id}", response_model=schemas.Item)

def deletar_item(item_id: int, db: Session = Depends(get_db)):

    deletado = crud.deletar_item(db, item_id)

    if deletado:

        return deletado

    return {"erro": "não encontrado"}

 