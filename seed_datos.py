from database import engine, Base
from models import Mesa, Voto
from database import SessionLocal

Base.metadata.create_all(bind=engine)
print("Tablas creadas")

db = SessionLocal()

db.query(Voto).delete()
db.query(Mesa).delete()

mesa_21 = Mesa(id=1, nombre="Mesa 21", electores=50)
mesa_22 = Mesa(id=2, nombre="Mesa 22", electores=55)
mesa_23 = Mesa(id=3, nombre="Mesa 23", electores=30)
mesa_24 = Mesa(id=4, nombre="Mesa 24", electores=40)
mesa_25 = Mesa(id=5, nombre="Mesa 25", electores=45)
mesa_26 = Mesa(id=6, nombre="Mesa 26", electores=35)
db.add_all([mesa_21, mesa_22, mesa_23, mesa_24, mesa_25, mesa_26])

votos = [
    Voto(mesa_id=1, agrupacion="Alternativa Académica", cantidad=20),
    Voto(mesa_id=1, agrupacion="La 15", cantidad=15),
    Voto(mesa_id=1, agrupacion="La Ues", cantidad=10),

    Voto(mesa_id=2, agrupacion="Alternativa Académica", cantidad=30),
    Voto(mesa_id=2, agrupacion="La 15", cantidad=20),
    Voto(mesa_id=2, agrupacion="La Ues", cantidad=10),

    Voto(mesa_id=3, agrupacion="Alternativa Académica", cantidad=10),
    Voto(mesa_id=3, agrupacion="La 15", cantidad=10),
    Voto(mesa_id=3, agrupacion="La Ues", cantidad=10),

    Voto(mesa_id=4, agrupacion="Alternativa Académica", cantidad=12),
    Voto(mesa_id=4, agrupacion="La 15", cantidad=10),
    Voto(mesa_id=4, agrupacion="La Ues", cantidad=8),

    Voto(mesa_id=5, agrupacion="Alternativa Académica", cantidad=35),
    Voto(mesa_id=5, agrupacion="La 15", cantidad=3),
    Voto(mesa_id=5, agrupacion="La Ues", cantidad=2),

    Voto(mesa_id=6, agrupacion="Alternativa Académica", cantidad=8),
    Voto(mesa_id=6, agrupacion="La 15", cantidad=9),
    Voto(mesa_id=6, agrupacion="La Ues", cantidad=7),
]
db.add_all(votos)

db.commit()
print("Datos cargados con éxito")
db.close()