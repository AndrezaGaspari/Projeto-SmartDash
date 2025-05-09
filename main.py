from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from banco_de_dados.database import Engine, Base, SessionLocal
from banco_de_dados import crud, schemas #temporariamente até ativar o crud.py
#from banco_de_dados import schemas
from cruds import CadastroRevendedor
from cruds import CadastroProdutos
from cruds import CadastroLojas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Middleware de CORS

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Cria tabelas no banco de dados
Base.metadata.create_all(bind=Engine)

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- ROTAS DE REVENDEDORES -------------------

@app.post("/revendedores", response_model=schemas.Revendedor)
def criar_revendedor(revendedor: schemas.RevendedorCreate, db: Session = Depends(get_db)):
    return CadastroRevendedor.criar_revendedor(db, revendedor)

@app.get("/revendedores", response_model=list[schemas.Revendedor])
def listar_revendedores(db: Session = Depends(get_db)):
    return CadastroRevendedor.listar_revendedores(db)

@app.get("/revendedores/{rev_id}", response_model=schemas.Revendedor)
def buscar_revendedor(rev_id: int, db: Session = Depends(get_db)):
    rev = CadastroRevendedor.buscar_revendedor(db, rev_id)
    if rev is None:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return rev

@app.put("/revendedores/{rev_id}", response_model=schemas.Revendedor)
def atualizar_revendedor(rev_id: int, revendedor: schemas.RevendedorCreate, db: Session = Depends(get_db)):
    rev = CadastroRevendedor.atualizar_revendedor(db, rev_id, revendedor)
    if rev is None:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return rev

@app.delete("/revendedores/{rev_id}", response_model=schemas.Revendedor)
def deletar_revendedor(rev_id: int, db: Session = Depends(get_db)):
    rev = CadastroRevendedor.deletar_revendedor(db, rev_id)
    if rev is None:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return rev

# ------------------- ROTAS DE PRODUTOS -------------------


@app.post("/produtos", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return CadastroProdutos.criar_produto(db, produto)


@app.get("/produtos", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return CadastroProdutos.listar_produtos(db)

@app.get("/produtos/{prod_id}", response_model=schemas.Produto)
def buscar_produto(prod_id: int, db: Session = Depends(get_db)):
    prod = CadastroProdutos.buscar_produto(db, prod_id)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@app.put("/produtos/{prod_id}", response_model=schemas.Produto)
def atualizar_produto(prod_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    prod = CadastroProdutos.atualizar_produto(db, prod_id, produto)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@app.delete("/produtos/{prod_id}", response_model=schemas.Produto)
def deletar_produto(prod_id: int, db: Session = Depends(get_db)):
    prod = CadastroProdutos.deletar_produto(db, prod_id)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod


# ------------------- ROTAS DE ITENS -------------------

@app.get("/items", response_model=list[schemas.Produto])  # Alterado para Produto que é realmnete temos 
def pegar(db: Session = Depends(get_db)):
    return crud.listar_itens(db)

#@app.get("/items", response_model=list[schemas.Item])
#def pegar(db: Session = Depends(get_db)):
 #   return crud.listar_itens(db)

@app.post("/items", response_model=schemas.Item)
def criar_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.criar_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=schemas.Item)
def atualizar(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    atualizado = crud.atualizar_item(db, item_id, item)
    if atualizado:
        return atualizado
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.delete("/items/{item_id}", response_model=schemas.Item)
def deletar_item(item_id: int, db: Session = Depends(get_db)):
    deletado = crud.deletar_item(db, item_id)
    if deletado:
        return deletado
    raise HTTPException(status_code=404, detail="Item não encontrado")

'''
# ------------------- ROTAS DE LOJAS -------------------


@app.post("/lojas", response_model=schemas.Loja)
def criar_loja(loja: schemas.LojaCreate, db: Session = Depends(get_db)):
    return CadastroLojas.criar_loja(db, loja)


@app.get("/lojas", response_model=list[schemas.Loja])
def listar_lojas(db: Session = Depends(get_db)):
    return CadastroProdutos.listar_produtos(db)

@app.get("/produtos/{prod_id}", response_model=schemas.Produto)
def buscar_produto(prod_id: int, db: Session = Depends(get_db)):
    prod = CadastroProdutos.buscar_produto(db, prod_id)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@app.put("/produtos/{prod_id}", response_model=schemas.Produto)
def atualizar_produto(prod_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    prod = CadastroProdutos.atualizar_produto(db, prod_id, produto)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@app.delete("/produtos/{prod_id}", response_model=schemas.Produto)
def deletar_produto(prod_id: int, db: Session = Depends(get_db)):
    prod = CadastroProdutos.deletar_produto(db, prod_id)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

'''