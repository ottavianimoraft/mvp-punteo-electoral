from database import SessionLocal
from models import Mesa, Voto

db = SessionLocal()

mesas = db.query(Mesa).all()
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
for mesa in mesas:
    votos_mesa = db.query(Voto).filter(Voto.mesa_id == mesa.id).all()
    resultado = clasificar_mesa(mesa, votos_mesa)
    print(mesa.nombre, "-", resultado)