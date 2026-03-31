from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Nanomaterial(Base):
    __tablename__ = "nanomateriales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    propiedades = Column(String)
    aplicacion = Column(String)
    estado = Column(String, nullable=False, default="ACTIVO")
    created_at = Column(DateTime, default=datetime.utcnow)