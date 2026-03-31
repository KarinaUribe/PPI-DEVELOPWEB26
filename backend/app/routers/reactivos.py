from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reactivo import Reactivo
from app.schemas.reactivo import ReactivoCreate, ReactivoResponse

router = APIRouter()

@router.post("/", response_model=ReactivoResponse)
def create_reactivo(reactivo: ReactivoCreate, db: Session = Depends(get_db)):
    db_reactivo = Reactivo(**reactivo.dict())
    db.add(db_reactivo)
    db.commit()
    db.refresh(db_reactivo)
    return db_reactivo


@router.get("/", response_model=list[ReactivoResponse])
def get_reactivos(db: Session = Depends(get_db)):
    return db.query(Reactivo).all()