from pydantic import BaseModel, Field, model_validator


class VotoEntrada(BaseModel):
    agrupacion: str = Field(min_length=1)
    cantidad: int = Field(ge=0)


class MesaEntrada(BaseModel):
    nombre: str = Field(min_length=1)
    electores: int = Field(gt=0)
    votos: list[VotoEntrada] = Field(min_length=1)

    @model_validator(mode="after")
    def al_menos_un_voto(self):
        if sum(v.cantidad for v in self.votos) == 0:
            raise ValueError("La mesa debe tener al menos un voto registrado")
        return self
    