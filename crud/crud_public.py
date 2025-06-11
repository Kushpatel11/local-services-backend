from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models import ServiceProvider, ProviderAddress


def search_providers_by_location(
    db: Session,
    area: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[ServiceProvider]:
    query = (
        db.query(ServiceProvider)
        .join(ServiceProvider.addresses)
        .filter(
            ServiceProvider.is_approved == True, ServiceProvider.is_deleted == False
        )
        .options(joinedload(ServiceProvider.addresses))
    )
    if area:
        query = query.filter(ProviderAddress.district.ilike(f"%{area}%"))
    if city:
        query = query.filter(ProviderAddress.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(ProviderAddress.state.ilike(f"%{state}%"))

    providers = query.offset(offset).limit(limit).all()
    return providers
