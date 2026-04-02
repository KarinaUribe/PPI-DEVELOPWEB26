from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class OrdenSintesis(Base):
    __tablename__ = "ordenes_sintesis"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    nanomaterial_id = Column(Integer, ForeignKey("nanomateriales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipamientos.id"), nullable=False)
    estado = Column(String, nullable=False, default="BORRADOR")
    observaciones = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reactivos = relationship("OrdenReactivo", back_populates="orden", cascade="all, delete-orphan")


class OrdenReactivo(Base):
    __tablename__ = "orden_reactivos"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes_sintesis.id"), nullable=False)
    reactivo_id = Column(Integer, ForeignKey("reactivos.id"), nullable=False)
    cantidad_requerida = Column(Float, nullable=False)

    orden = relationship("OrdenSintesis", back_populates="reactivos")