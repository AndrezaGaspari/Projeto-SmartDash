from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from banco_de_dados.database import Engine, Base, SessionLocal
from banco_de_dados import schemas
from cruds import CadastroRevendedor,CarrinhoProdutos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Libera para todos os domínios
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

# ------------------- ROTAS DE ITENS -------------------

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