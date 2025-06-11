from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.rating_schemas import ServiceRatingOut
from crud.crud_ratings import get_service_reviews
from typing import List

router = APIRouter()


@router.get("/{service_id}/reviews", response_model=List[ServiceRatingOut])
def list_service_reviews(service_id: int, db: Session = Depends(get_db)):
    return get_service_reviews(db, service_id=service_id)
