from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "clave-secreta-de-prueba-ds4p"
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