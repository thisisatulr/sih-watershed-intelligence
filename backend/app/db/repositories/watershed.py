import uuid

from geoalchemy2 import Geography
from geoalchemy2.elements import WKTElement
from sqlalchemy import cast, func, select
from sqlalchemy.orm import Session

from ...models.watershed import Watershed

def get_watershed_by_id(db: Session, watershed_id: uuid.UUID) -> Watershed | None:
    return db.get(Watershed, watershed_id)

def get_watersheds(db: Session) -> list[Watershed]:
    return list(db.scalars(select(Watershed).order_by(Watershed.name)).all())

def create_watershed(
    db: Session,
    *,
    name: str,
    state: str,
    district: str,
    geometry_wkt: str,
    area_sq_km: float | None = None,
) -> Watershed:
    watershed = Watershed(
        name=name,
        state=state,
        district=district,
        area_sq_km=area_sq_km,
        geometry=WKTElement(geometry_wkt, srid=4326),
    )
    db.add(watershed)
    db.commit()
    db.refresh(watershed)
    return watershed

def get_watershed_area_sq_km(
    db: Session, watershed_id: uuid.UUID
) -> float | None:
    stmt = select(
        func.ST_Area(cast(Watershed.geometry, Geography)) / 1_000_000.0
    ).where(Watershed.id == watershed_id)

    value = db.scalar(stmt)
    return float(value) if value is not None else None

def get_watersheds_intersecting_wkt(
    db: Session, geometry_wkt: str
) -> list[Watershed]:
    geometry = WKTElement(geometry_wkt, srid=4326)
    stmt = (
        select(Watershed)
        .where(func.ST_Intersects(Watershed.geometry, geometry))
        .order_by(Watershed.name)
    )
    return list(db.scalars(stmt).all())
