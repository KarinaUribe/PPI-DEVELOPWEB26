from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
from datetime import datetime
from app.database import Base

class Reactivo(Base):
    __tablename__ = "reactivos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    cantidad_stock = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)
    fecha_vencimiento = Column(Date)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)