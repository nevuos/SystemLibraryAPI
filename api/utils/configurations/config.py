import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

# Importar pysqlcipher3
import pysqlcipher3.dbapi2 as sqlite

class Config(object):
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DB_FOLDER = os.path.join(os.getcwd(), "instance")
    DB_FILE = "library.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite+pysqlcipher://:{DATABASE_PASSWORD}@/{DB_FOLDER}/{DB_FILE}?cipher=aes-256-cfb&kdf_iter=64000'

# Abrir conexão com o banco de dados usando pysqlcipher3
def create_engine_with_cipher():
    os.makedirs(Config.DB_FOLDER, exist_ok=True)
    db_path = os.path.join(Config.DB_FOLDER, Config.DB_FILE)
    conn = sqlite.connect(db_path)
    conn.execute(f"PRAGMA key='{Config.DATABASE_PASSWORD}'")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, module=sqlite, echo=True)
    return engine

# Configurar o SQLAlchemy para usar o engine com o cipher
engine = create_engine_with_cipher()
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
