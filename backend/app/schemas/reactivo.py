from pydantic import BaseModel
from datetime import date

class ReactivoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    cantidad_stock: float
    unidad: str
    fecha_vencimiento: date

class ReactivoCreate(ReactivoBase):
    pass

class ReactivoResponse(ReactivoBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True