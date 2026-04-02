from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from datetime import datetime
from app.database import Base

class Equipamiento(Base):
    __tablename__ = "equipamientos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    estado = Column(String, nullable=False, default="DISPONIBLE")
    fecha_mantenimiento = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)