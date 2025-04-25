from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Caminho do banco de dados SQLite
DATABASE_URL = "sqlite:///./banco.db"

# Cria o "motor" de conexão com o banco
Engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria a base para as classes (modelos) que virarão tabelas no banco
Base = declarative_base()

# Cria uma sessão para interagir com o banco (sessão = conexão controlada)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
