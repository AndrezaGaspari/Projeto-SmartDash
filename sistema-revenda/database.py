from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# String de conexão (ajuste o nome do servidor se necessário)
DATABASE_URL = "mssql+pyodbc://localhost/sistema_revenda?driver=ODBC+Driver+17+for+SQL+Server"

# Criar engine e sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
