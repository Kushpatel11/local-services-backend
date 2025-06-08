from models import Service, ServiceProvider
from sqlalchemy.orm import Session


def create_service(db: Session, provider: dict, service_in):
    db_provider = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.email == provider["sub"])
        .first()
    )
    if not db_provider:
        raise ValueError("Provider not found or not authorized.")
    service = Service(
        title=service_in.title,
        provider_id=db_provider.id,
        service_category_id=service_in.service_category_id,
        description=service_in.description,
        min_price=service_in.min_price,
        max_price=service_in.max_price,
        available=service_in.available,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
