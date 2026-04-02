from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.orden import OrdenSintesis, OrdenReactivo
from app.models.nanomaterial import Nanomaterial
from app.models.reactivo import Reactivo
from app.models.equipamiento import Equipamiento
from app.schemas.orden import OrdenCreate, OrdenResponse, OrdenEstadoUpdate

router = APIRouter()

@router.post("/", response_model=OrdenResponse)
def create_orden(orden: OrdenCreate, db: Session = Depends(get_db)):
    nanomaterial = db.query(Nanomaterial).filter(Nanomaterial.id == orden.nanomaterial_id).first()
    if not nanomaterial:
        raise HTTPException(status_code=404, detail="Nanomaterial not found")
    if nanomaterial.estado != "ACTIVO":
        raise HTTPException(status_code=400, detail="Nanomaterial is not active")

    equipo = db.query(Equipamiento).filter(Equipamiento.id == orden.equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipamiento not found")
    if equipo.estado != "DISPONIBLE":
        raise HTTPException(status_code=400, detail="Equipamiento is not available")

    for item in orden.reactivos:
        reactivo = db.query(Reactivo).filter(Reactivo.id == item.reactivo_id).first()
        if not reactivo:
            raise HTTPException(status_code=404, detail=f"Reactivo {item.reactivo_id} not found")
        if reactivo.cantidad_stock < item.cantidad_requerida:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for reactivo {reactivo.nombre}")
        if reactivo.fecha_vencimiento and reactivo.fecha_vencimiento < date.today():
            raise HTTPException(status_code=400, detail=f"Reactivo {reactivo.nombre} is expired")

    nueva_orden = OrdenSintesis(
        codigo=orden.codigo,
        nanomaterial_id=orden.nanomaterial_id,
        usuario_id=orden.usuario_id,
        equipo_id=orden.equipo_id,
        observaciones=orden.observaciones,
        estado="BORRADOR"
    )

    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    for item in orden.reactivos:
        orden_reactivo = OrdenReactivo(
            orden_id=nueva_orden.id,
            reactivo_id=item.reactivo_id,
            cantidad_requerida=item.cantidad_requerida
        )
        db.add(orden_reactivo)

    db.commit()
    db.refresh(nueva_orden)

    return nueva_orden


@router.get("/", response_model=list[OrdenResponse])
def get_ordenes(db: Session = Depends(get_db)):
    return db.query(OrdenSintesis).all()


@router.patch("/{orden_id}/estado", response_model=OrdenResponse)
def update_estado_orden(orden_id: int, data: OrdenEstadoUpdate, db: Session = Depends(get_db)):
    orden = db.query(OrdenSintesis).filter(OrdenSintesis.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden not found")

    transiciones_validas = {
        "BORRADOR": ["APROBADA", "CANCELADA"],
        "APROBADA": ["EN_PROCESO", "CANCELADA"],
        "EN_PROCESO": ["COMPLETADA"],
        "COMPLETADA": [],
        "CANCELADA": []
    }

    if data.estado not in transiciones_validas.get(orden.estado, []):
        raise HTTPException(status_code=400, detail=f"Invalid transition from {orden.estado} to {data.estado}")

    if data.estado in ["APROBADA", "CANCELADA"] and data.role != "ADMINISTRADOR":
        raise HTTPException(status_code=403, detail="Only ADMINISTRADOR can approve or cancel orders")

    if data.estado == "COMPLETADA":
        reactivos_orden = db.query(OrdenReactivo).filter(OrdenReactivo.orden_id == orden.id).all()

        for item in reactivos_orden:
            reactivo = db.query(Reactivo).filter(Reactivo.id == item.reactivo_id).first()
            if reactivo.cantidad_stock < item.cantidad_requerida:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for reactivo {reactivo.nombre}")
            reactivo.cantidad_stock -= item.cantidad_requerida

    orden.estado = data.estado
    db.commit()
    db.refresh(orden)

    return orden