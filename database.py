import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# La dirección de la base viene de una variable de entorno.
# Si no existe, se usa el archivo SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///elecciones_mvp.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()