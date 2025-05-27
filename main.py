from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from banco_de_dados.database import Engine, Base, SessionLocal
from banco_de_dados import schemas
from cruds import CadastroRevendedor, CarrinhoProdutos, CadastroProdutos, CadastroLojas
from fastapi.middleware.cors import CORSMiddleware # Certifique-se desta importação
from banco_de_dados.schemas import LoginRevendedor , LoginLoja


app = FastAPI()

# --- SEÇÃO DE CONFIGURAÇÃO CORS ---
origins = [
    "http://localhost:5173",  # ONDE SEU FRONTEND VUE ESTÁ RODANDO
    "http://127.0.0.1:5173",  # E ESTA TAMBÉM É IMPORTANTE
    "http://localhost:8080",  # Se você usa Vue CLI em vez de Vite, pode ser 8080
    "http://127.0.0.1:8080",
    # Adicione outras origens se necessário, por exemplo, o domínio de produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Use a lista de origens definida acima
    allow_credentials=True,        # Permite cookies/cabeçalhos de autorização
    allow_methods=["*"],           # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Permite todos os cabeçalhos
)
# --- FIM DA SEÇÃO DE CONFIGURAÇÃO CORS ---


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

@app.post("/login")
def login(dados: LoginRevendedor, db: Session = Depends(get_db)):
    usuario = CadastroRevendedor.verificar_login(db, dados.email, dados.senha)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    return True



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

# NOVO: Endpoint para login de lojas
@app.post("/lojas/login") # <--- NOVO ENDPOINT DE LOGIN PARA LOJAS
def login_loja(dados: LoginLoja, db: Session = Depends(get_db)):
    loja = CadastroLojas.verificar_login_loja(db, dados.email, dados.senha)
    if loja is None:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos para a loja")
    # Retorna dados úteis para o frontend
    return {"message": "Login de loja bem-sucedido!", "id": loja.id, "email": loja.email, "nome_fantasia": loja.nome_fantasia}







@app.post("/", response_model=schemas.CarrinhoProduto)
def adicionar_produto(item: schemas.CarrinhoProdutoCreate, db: Session = Depends(get_db)):
    return CarrinhoProdutos.adicionar_Produto_carrinho(db, item)


@app.get("/carrinho/{revendedor_id}", response_model=list[schemas.CarrinhoProduto])
def listar_itens(revendedor_id: int, db: Session = Depends(get_db)):
    return CarrinhoProdutos.listar_Produto_carrinho(db, revendedor_id)

@app.delete("/carrinho/item/{revendedor_id}/{produto_id}")
def remover_item_path(revendedor_id: int, produto_id: int, db: Session = Depends(get_db)):
    sucesso = CarrinhoProdutos.remover_Produto_carrinho(db, revendedor_id, produto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"detail": "Item removido com sucesso"}



@app.delete("/carrinho/limpar/{revendedor_id}")
def limpar_carrinho(revendedor_id: int, db: Session = Depends(get_db)):
    CarrinhoProdutos.limpar_carrinho(db, revendedor_id)
    return {"detail": "Carrinho limpo com sucesso"}
