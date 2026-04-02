from pydantic import BaseModel
from typing import List

class OrdenReactivoCreate(BaseModel):
    reactivo_id: int
    cantidad_requerida: float

class OrdenCreate(BaseModel):
    codigo: str
    nanomaterial_id: int
    usuario_id: int
    equipo_id: int
    observaciones: str | None = None
    reactivos: List[OrdenReactivoCreate]

class OrdenEstadoUpdate(BaseModel):
    estado: str
    role: str

class OrdenReactivoResponse(BaseModel):
    id: int
    reactivo_id: int
    cantidad_requerida: float

    class Config:
        from_attributes = True

class OrdenResponse(BaseModel):
    id: int
    codigo: str
    nanomaterial_id: int
    usuario_id: int
    equipo_id: int
    estado: str
    observaciones: str | None = None
    reactivos: List[OrdenReactivoResponse] = []

    class Config:
        from_attributes = True