
# Este archivo define el router para el dashboard
# para obtener un resumen de los datos en el sistema(laboratorio)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database import get_db
from app.models.reactivo import Reactivo
from app.models.nanomaterial import Nanomaterial
from app.models.equipamiento import Equipamiento
from app.models.orden import OrdenSintesis

router = APIRouter()

@router.get("/resumen")
def dashboard_resumen(db: Session = Depends(get_db)):

    total_reactivos = db.query(Reactivo).count()

    fecha_limite = date.today() + timedelta(days=30)
    reactivos_por_vencer = db.query(Reactivo).filter(
        Reactivo.fecha_vencimiento <= fecha_limite
    ).count()

    nanomateriales_activos = db.query(Nanomaterial).filter(
        Nanomaterial.estado == "ACTIVO"
    ).count()

    equipos_disponibles = db.query(Equipamiento).filter(
        Equipamiento.estado == "DISPONIBLE"
    ).count()

    ordenes_borrador = db.query(OrdenSintesis).filter(
        OrdenSintesis.estado == "BORRADOR"
    ).count()

    ordenes_proceso = db.query(OrdenSintesis).filter(
        OrdenSintesis.estado == "EN_PROCESO"
    ).count()

    ordenes_completadas = db.query(OrdenSintesis).filter(
        OrdenSintesis.estado == "COMPLETADA"
    ).count()

    return {
        "reactivos": {
            "total": total_reactivos,
            "por_vencer": reactivos_por_vencer
        },
        "nanomateriales": {
            "activos": nanomateriales_activos
        },
        "equipos": {
            "disponibles": equipos_disponibles
        },
        "ordenes": {
            "borrador": ordenes_borrador,
            "en_proceso": ordenes_proceso,
            "completadas": ordenes_completadas
        }
    }