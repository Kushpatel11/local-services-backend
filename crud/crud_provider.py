from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from models import ProviderAddress, ServiceProvider, ServiceCategory
from schemas.provider_schemas import ServiceProviderCreate, ProviderUpdate
from utils.hashing import verify_password
from core.security import create_access_token
from sqlalchemy.future import select
from utils.hashing import hash_password


# crud/provider.py


def register_provider(db: Session, provider_data: ServiceProviderCreate):
    category = (
        db.query(ServiceCategory)
        .filter(ServiceCategory.id == provider_data.service_category_id)
        .first()
    )
    if not category:
        raise HTTPException(
            status_code=400,  # Bad Request
            detail="Invalid service_category_id: not found.",
        )
    hashed_password = hash_password(provider_data.password)
    provider = ServiceProvider(
        name=provider_data.name,
        mobile=provider_data.mobile,
        email=provider_data.email,
        password_hash=hashed_password,
        experience_years=provider_data.experience_years,
        service_category_id=provider_data.service_category_id,
        is_approved=False,  # 🛑 Needs admin approval
        is_deleted=False,
        deleted_at=None,
    )
    db.add(provider)
    db.flush()

    for addr in provider_data.addresses:
        address = ProviderAddress(
            provider_id=provider.id,
            city=addr.city,
            district=addr.district,
            state=addr.state,
            country=addr.country,
            pincode=addr.pincode,
            latitude=addr.latitude,
            longitude=addr.longitude,
            label=addr.label,
        )
        db.add(address)

    db.commit()
    db.refresh(provider)
    return provider


def provider_login(form_data, db):
    result = db.execute(
        select(ServiceProvider).where(ServiceProvider.email == form_data.username)
    )
    db_user = result.scalars().first()
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": db_user.email, "role": "provider"})
    return {"access_token": access_token, "token_type": "bearer"}


def update_profile(update_data, db, provider):
    db_user = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.email == provider["sub"])
        .first()
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="Provider not found")

    for field, value in update_data.dict(exclude_unset=True).items():
        if field == "addresses" and value:
            for addr_update in value:
                if db_user.addresses:
                    addr = db_user.addresses[0]
                    for a_field, a_value in addr_update.items():  # FIXED: no .dict()
                        setattr(addr, a_field, a_value)
                else:
                    new_addr = ProviderAddress(
                        provider_id=db_user.id, **addr_update  # FIXED: no .dict()
                    )
                    db.add(new_addr)
        elif value is not None:
            setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_own_profile(
    db,
    provider,
):
    db_provider = (
        db.query(ServiceProvider)
        .filter(
            ServiceProvider.email == provider["sub"],
            ServiceProvider.is_deleted == False,
        )
        .first()
    )
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    # Soft delete
    db_provider.is_deleted = True
    db_provider.deleted_at = datetime.utcnow()
    db.commit()
    return None
