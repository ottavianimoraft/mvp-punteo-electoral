import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext

load_dotenv()

# La clave secreta viene de una variable de entorno (archivo .env)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Falta la variable de entorno SECRET_KEY")

ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_password(password_plana, password_hash):
    return pwd_context.verify(password_plana, password_hash)


def crear_token(username):
    expiracion = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION)
    datos = {"sub": username, "exp": expiracion}
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


def leer_token(token):
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return datos.get("sub")
    except JWTError:
        return None