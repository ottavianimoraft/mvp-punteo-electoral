from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from models import Mesa, Voto, Usuario
from seguridad import verificar_password, crear_token, leer_token
from esquemas import MesaEntrada
import joblib

app = FastAPI(
    title="API de Detección de Punteo Electoral",
    description="Backend para consultar mesas y alertas de irregularidades en elecciones universitarias.",
    version="1.0.0",
    contact={
        "name": "Juan Ignacio Gonzalez Bracco y Mora Ottaviani",
    },
)

modelo_riesgo = joblib.load("modelo_riesgo.pkl")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def usuario_actual(token: str = Depends(oauth2_scheme)):
    username = leer_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Token inválido o vencido")
    return username


def clasificar_mesa(mesa, votos_mesa):
    total_votos = sum(v.cantidad for v in votos_mesa)

    if total_votos > mesa.electores:
        return "ALERTA: más votos que electores"

    if total_votos == mesa.electores:
        return "revisar: 100% de participación"

    for v in votos_mesa:
        porcentaje = v.cantidad / total_votos
        if porcentaje > 0.70:
            return f"ALERTA: concentración anómala ({v.agrupacion} tiene el {porcentaje:.0%})"

    return "OK"


@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente - Proyecto DS4P"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == form.username).first()
    db.close()

    if usuario is None or not verificar_password(form.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token(usuario.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/mesas")
def listar_mesas(usuario: str = Depends(usuario_actual)):
    db = SessionLocal()
    mesas = db.query(Mesa).all()
    resultado = [{"id": m.id, "nombre": m.nombre, "electores": m.electores} for m in mesas]
    db.close()
    return resultado


@app.get("/alertas")
def listar_alertas(usuario: str = Depends(usuario_actual)):
    db = SessionLocal()
    mesas = db.query(Mesa).all()

    resultado = []
    for mesa in mesas:
        votos_mesa = db.query(Voto).filter(Voto.mesa_id == mesa.id).all()
        estado = clasificar_mesa(mesa, votos_mesa)
        if estado != "OK":
            resultado.append({"mesa": mesa.nombre, "estado": estado})

    db.close()
    return resultado


@app.get("/prediccion/{mesa_id}")
def predecir_riesgo(mesa_id: int, usuario: str = Depends(usuario_actual)):
    db = SessionLocal()
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    votos_mesa = db.query(Voto).filter(Voto.mesa_id == mesa_id).all()
    db.close()

    if mesa is None:
        return {"error": "Mesa no encontrada"}

    total_votos = sum(v.cantidad for v in votos_mesa)
    concentracion_max = max(v.cantidad / total_votos for v in votos_mesa)

    participacion = total_votos / mesa.electores
    entrada = [[participacion, concentracion_max]]
    prediccion = modelo_riesgo.predict(entrada)[0]

    return {
        "mesa": mesa.nombre,
        "riesgo_predicho": "ALTO" if prediccion == 1 else "BAJO"
    }


@app.post("/mesas", status_code=201)
def crear_mesa(mesa_nueva: MesaEntrada, usuario: str = Depends(usuario_actual)):
    db = SessionLocal()

    # Rechazar nombres repetidos
    existente = db.query(Mesa).filter(Mesa.nombre == mesa_nueva.nombre).first()
    if existente is not None:
        db.close()
        raise HTTPException(status_code=409, detail="Ya existe una mesa con ese nombre")

    nueva = Mesa(nombre=mesa_nueva.nombre, electores=mesa_nueva.electores)
    db.add(nueva)
    db.flush()

    votos_nuevos = [
        Voto(mesa_id=nueva.id, agrupacion=v.agrupacion, cantidad=v.cantidad)
        for v in mesa_nueva.votos
    ]
    db.add_all(votos_nuevos)
    db.commit()

    estado = clasificar_mesa(nueva, votos_nuevos)
    resultado = {"id": nueva.id, "nombre": nueva.nombre, "estado": estado}
    db.close()
    return resultado


@app.get("/resumen")
def resumen(usuario: str = Depends(usuario_actual)):
    db = SessionLocal()
    mesas = db.query(Mesa).all()

    resultado = []
    for mesa in mesas:
        votos_mesa = db.query(Voto).filter(Voto.mesa_id == mesa.id).all()
        total = sum(v.cantidad for v in votos_mesa)
        estado = clasificar_mesa(mesa, votos_mesa) if total > 0 else "sin votos"
        resultado.append({
            "id": mesa.id,
            "nombre": mesa.nombre,
            "electores": mesa.electores,
            "total_votos": total,
            "participacion": round(total / mesa.electores * 100, 1),
            "estado": estado,
            "votos": {v.agrupacion: v.cantidad for v in votos_mesa},
        })

    db.close()
    return resultado
