import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.layer import LayerMetadata

def get_layer_by_id(db: Session, layer_id: uuid.UUID) -> LayerMetadata | None:
    return db.get(LayerMetadata, layer_id)

def get_layers(db: Session) -> list[LayerMetadata]:
    return list(db.scalars(select(LayerMetadata).order_by(LayerMetadata.name)).all())

def get_layers_by_type(db: Session, layer_type: str) -> list[LayerMetadata]:
    stmt = (
        select(LayerMetadata)
        .where(LayerMetadata.layer_type == layer_type)
        .order_by(LayerMetadata.name)
    )
    return list(db.scalars(stmt).all())
