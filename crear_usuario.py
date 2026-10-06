from database import SessionLocal, engine, Base
from models import Usuario
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

username = "admin"
password_plana = "ds4p2026"

password_encriptada = pwd_context.hash(password_plana)

usuario_existente = db.query(Usuario).filter(Usuario.username == username).first()
if usuario_existente:
    print("Ese usuario ya existe")
else:
    nuevo_usuario = Usuario(username=username, password_hash=password_encriptada)
    db.add(nuevo_usuario)
    db.commit()
    print(f"Usuario '{username}' creado con éxito")
    print("Contraseña guardada (encriptada):", password_encriptada)

db.close()