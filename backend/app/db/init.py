from .base import Base
from .session import engine
from ..models import LayerMetadata, Watershed  # noqa: F401

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
