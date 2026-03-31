from pydantic import BaseModel

class NanomaterialBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    propiedades: str | None = None
    aplicacion: str | None = None
    estado: str = "ACTIVO"

class NanomaterialCreate(NanomaterialBase):
    pass

class NanomaterialResponse(NanomaterialBase):
    id: int

    class Config:
        from_attributes = True