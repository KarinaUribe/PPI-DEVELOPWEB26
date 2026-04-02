from pydantic import BaseModel
from datetime import date

class EquipamientoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    estado: str = "DISPONIBLE"
    fecha_mantenimiento: date | None = None

class EquipamientoCreate(EquipamientoBase):
    pass

class EquipamientoResponse(EquipamientoBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True