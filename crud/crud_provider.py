from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import ServiceProvider
from typing import List


def get_approved_providers(db: Session) -> List[ServiceProvider]:
    return db.query(ServiceProvider).filter(ServiceProvider.is_approved == True).all()


def get_provider_by_id(db: Session, provider_id: int) -> ServiceProvider:
    provider = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.id == provider_id, ServiceProvider.is_approved == True)
        .first()
    )
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service provider not found"
        )
    return provider
