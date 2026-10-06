from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    electores = Column(Integer, nullable=False)


class Voto(Base):
    __tablename__ = "votos"

    id = Column(Integer, primary_key=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    agrupacion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)