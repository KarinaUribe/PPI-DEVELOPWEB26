from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipamiento import Equipamiento
from app.schemas.equipamiento import EquipamientoCreate, EquipamientoResponse

router = APIRouter()

@router.post("/", response_model=EquipamientoResponse)
def create_equipamiento(equipamiento: EquipamientoCreate, db: Session = Depends(get_db)):
    db_equipamiento = Equipamiento(**equipamiento.dict())
    db.add(db_equipamiento)
    db.commit()
    db.refresh(db_equipamiento)
    return db_equipamiento

@router.get("/", response_model=list[EquipamientoResponse])
def get_equipamientos(db: Session = Depends(get_db)):
    return db.query(Equipamiento).all()