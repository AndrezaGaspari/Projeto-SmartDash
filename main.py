from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from banco_de_dados.database import Engine, Base, SessionLocal
from banco_de_dados import schemas #temporariamente até ativar o crud.py
#from banco_de_dados import schemas
from cruds import CadastroRevendedor,CarrinhoProdutos
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

# ------------------- ROTAS DO CARRINHO -------------------

'''@app.get("/carrinho", response_model=schemas.Pedido)
def lista_carrinho(db: Session = Depends(get_db)):
    return CarrinhoProdutos.listar_carrinho


@app.post("/carrinho", response_model=schemas.Pedido)
def criar_carrinho(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return CarrinhoProdutos.criar_carrinho(db,pedido)


@app.put("/carrinho/{rev_id}", response_model=schemas.Pedido)
def atualizar_carrinho(rev_id = int, db: Session = Depends(get_db), revendedor = schemas.RevendedorCreates):
    rev = CarrinhoProdutos.atualizar_carrinho(rev_id, db, revendedor)
    if rev is None:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return rev

@app.delete("/carrinho/{rev_id}", response_model=schemas.Pedido)
def atualizar_carrinho(rev_id = int, db: Session = Depends(get_db)):
    rev = CadastroRevendedor.deletar_Carrinho(db, rev_id)
    if rev is None:
        raise HTTPException(status_code=404, detail="Revendedor não encontrado")
    return rev'''

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

# ------------------- ROTAS DE LOJAS -------------------


@app.post("/lojas", response_model=schemas.Loja)
def criar_loja(loja: schemas.LojaCreate, db: Session = Depends(get_db)):
    return CadastroLojas.criar_loja(db, loja)


@app.get("/lojas", response_model=list[schemas.Loja])
def listar_lojas(db: Session = Depends(get_db)):
    return CadastroLojas.listar_lojas(db)

@app.get("/lojas/{loj_id}", response_model=schemas.Loja)
def buscar_loja(loj_id: int, db: Session = Depends(get_db)):
    loj = CadastroLojas.buscar_lojas(db, loj_id)
    if loj is None:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return loj

@app.put("/lojas/{loj_id}", response_model=schemas.Loja)
def atualizar_loja(loj_id: int, loja: schemas.LojaCreate, db: Session = Depends(get_db)):
    loj = CadastroLojas.atualizar_lojas(db, loj_id, loja)
    if loj is None:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return loj

@app.delete("/lojas/{loj_id}", response_model=schemas.Loja)
def deletar_loja(loj_id: int, db: Session = Depends(get_db)):
    loj = CadastroLojas.deletar_loja(db, loj_id)
    if loj is None:
        raise HTTPException(status_code=404, detail="Loja não encontradao")
    return loj