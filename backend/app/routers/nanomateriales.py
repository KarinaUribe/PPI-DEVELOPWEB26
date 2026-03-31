from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.nanomaterial import Nanomaterial
from app.schemas.nanomaterial import NanomaterialCreate, NanomaterialResponse

router = APIRouter()

@router.post("/", response_model=NanomaterialResponse)
def create_nanomaterial(nanomaterial: NanomaterialCreate, db: Session = Depends(get_db)):
    db_nanomaterial = Nanomaterial(**nanomaterial.dict())
    db.add(db_nanomaterial)
    db.commit()
    db.refresh(db_nanomaterial)
    return db_nanomaterial

@router.get("/", response_model=list[NanomaterialResponse])
def get_nanomateriales(db: Session = Depends(get_db)):
    return db.query(Nanomaterial).all()