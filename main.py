from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form # Importe UploadFile, File e Form
from sqlalchemy.orm import Session
from banco_de_dados.database import Engine, Base, SessionLocal
from banco_de_dados import schemas
from cruds import CadastroRevendedor, CarrinhoProdutos, CadastroProdutos, CadastroLojas
from fastapi.middleware.cors import CORSMiddleware
from banco_de_dados.schemas import LoginRevendedor , LoginLoja
from fastapi.staticfiles import StaticFiles
import os 
from typing import Optional 
from datetime import date

app = FastAPI()

# CONFIGURAÇÃO CORS 
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração imagens estaticas

UPLOAD_DIRECTORY = "./static/images"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Monta o diretório estatico 
app.mount("/static", StaticFiles(directory="static"), name="static")



# tabela banco de dados criada 
Base.metadata.create_all(bind=Engine)

# Dependência bd 
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
    # Retorna o ID do revendedor para o frontend
    return {"message": "Login de revendedor bem-sucedido!", "id": usuario.id, "email": usuario.email, "nome": usuario.nome}


# ------------------- ROTAS DE PRODUTOS  -------------------

@app.post("/produtos", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
async def criar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    valor_produto: float = Form(...),
    quantidade: int = Form(...),
    vencimento: Optional[date] = Form(None), 
    fabricacao: Optional[date] = Form(None), 
    disponivel: bool = Form(True), 
    fk_loja_id: int = Form(...),
    imagem: Optional[UploadFile] = File(None), 
    db: Session = Depends(get_db)
):
    image_url = None
    if imagem:
        # Gera um nome de arquivo único para evitar colisões
        import uuid
        file_extension = os.path.splitext(imagem.filename)[1] # Pega a extensão (.jpg, .png)
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

       
        try:



            with open(file_path, "wb") as buffer:
                # Lê o arquivo em pedaços para lidar com arquivos grandes
                while contents := await imagem.read(1024 * 1024): 
                    buffer.write(contents)
            
            # Define a URL que será salva no banco e retornada para o frontend
            image_url = f"/static/images/{unique_filename}"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao salvar imagem: {e}")

    # Cria o produto no banco de dados.

    db_produto_data = {
        "nome": nome,
        "descricao": descricao,
        "categoria": categoria,
        "valor_produto": valor_produto,
        "quantidade": quantidade,
        "vencimento": vencimento,
        "fabricacao": fabricacao,
        "imagem": image_url, # <<< A URL da imagem salva
        "disponivel": disponivel,
        "fk_loja_id": fk_loja_id
    }
    
    # Cria uma instância do schema ProdutoCreate para validar os dados
    produto_schema_instance = schemas.ProdutoCreate(**db_produto_data)

    # Chama a função de CRUD, que agora deve aceitar um schema.ProdutoCreate
    return CadastroProdutos.criar_produto(db, produto_schema_instance)


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
        raise HTTPException(status_code=404, detail="Loja não encontradao")
    return loj

@app.delete("/lojas/{loj_id}", response_model=schemas.Loja)
def deletar_loja(loj_id: int, db: Session = Depends(get_db)):
    loj = CadastroLojas.deletar_loja(db, loj_id)
    if loj is None:
        raise HTTPException(status_code=404, detail="Loja não encontradao")
    return loj

@app.post("/lojas/login")
def login_loja(dados: LoginLoja, db: Session = Depends(get_db)):
    loja = CadastroLojas.verificar_login_loja(db, dados.email, dados.senha)
    if loja is None:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos para a loja")
    return {"message": "Login de loja bem-sucedido!", "id": loja.id, "email": loja.email, "nome_fantasia": loja.nome_fantasia}


# ------------------- ROTAS DE CARRINHO -------------------

@app.post("/carrinho/adicionar", response_model=schemas.CarrinhoProduto, status_code=status.HTTP_201_CREATED)
def adicionar_produto_carrinho(item: schemas.CarrinhoProdutoCreate, db: Session = Depends(get_db)):
    return CarrinhoProdutos.adicionar_Produto_carrinho(db, item)

@app.get("/carrinho/{revendedor_id}", response_model=list[schemas.CarrinhoProdutoDisplay]) 
def listar_itens_carrinho(revendedor_id: int, db: Session = Depends(get_db)):
    return CarrinhoProdutos.listar_Produto_carrinho(db, revendedor_id)

@app.delete("/carrinho/item/{revendedor_id}/{produto_id}")
def remover_item_carrinho(revendedor_id: int, produto_id: int, db: Session = Depends(get_db)):
    sucesso = CarrinhoProdutos.remover_Produto_carrinho(db, revendedor_id, produto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")
    return {"detail": "Item removido com sucesso do carrinho"}

@app.delete("/carrinho/limpar/{revendedor_id}")
def limpar_carrinho_completo(revendedor_id: int, db: Session = Depends(get_db)):
    CarrinhoProdutos.limpar_carrinho(db, revendedor_id)
    return {"detail": "Carrinho limpo com sucesso"}
