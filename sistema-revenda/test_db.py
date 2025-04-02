from database import SessionLocal

try:
    db = SessionLocal()
    print("Conexão com SQL Server bem-sucedida!")
    db.close()
except Exception as e:
    print("Erro ao conectar ao banco:", e)
