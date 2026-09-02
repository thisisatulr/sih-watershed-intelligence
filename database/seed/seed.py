import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.db.init import init_db
from app.db.repositories.layer import get_layers
from app.db.repositories.watershed import (
    create_watershed,
    get_watershed_area_sq_km,
)
from app.db.session import SessionLocal

DEMO_WATERSHED_WKT = (
    "MULTIPOLYGON (((76.9000 10.0000, "
    "76.9000 10.1000, "
    "77.0000 10.1000, "
    "77.0000 10.0000, "
    "76.9000 10.0000)))"
)

def main() -> None:
    init_db()

    with SessionLocal() as db:
        existing = get_layers(db)

        if not existing:
            from app.models.layer import LayerMetadata

            db.add(
                LayerMetadata(
                    name="Demo Rainfall Layer",
                    layer_type="rainfall",
                    description="Synthetic development-only layer metadata.",
                    source="demo",
                    version="1.0",
                    metadata_json={"official": False},
                )
            )
            db.commit()

        watershed = create_watershed(
            db,
            name="Demo Watershed",
            state="DEMO",
            district="DEMO",
            geometry_wkt=DEMO_WATERSHED_WKT,
        )

        area = get_watershed_area_sq_km(db, watershed.id)
        watershed.area_sq_km = area
        db.commit()

        print(f"Created demo watershed: {watershed.id}")
        print(f"Calculated area: {area:.4f} sq km")

if __name__ == "__main__":
    main()
