import uuid

import pytest
from sqlalchemy import text

from backend.app.db.init import init_db
from backend.app.db.repositories.watershed import (
    create_watershed,
    get_watershed_area_sq_km,
    get_watershed_by_id,
    get_watersheds_intersecting_wkt,
)
from backend.app.db.session import SessionLocal

TEST_WKT = (
    "MULTIPOLYGON (((76.9000 10.0000, "
    "76.9000 10.1000, "
    "77.0000 10.1000, "
    "77.0000 10.0000, "
    "76.9000 10.0000)))"
)

@pytest.fixture(scope="module", autouse=True)
def database():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT PostGIS_Version()"))
        init_db()
    except Exception as exc:
        pytest.skip(f"PostgreSQL/PostGIS unavailable: {exc}")

def test_postgis_is_available():
    with SessionLocal() as db:
        version = db.scalar(text("SELECT PostGIS_Version()"))
        assert version

def test_watershed_round_trip():
    watershed_id = None
    with SessionLocal() as db:
        watershed = create_watershed(
            db,
            name=f"Test Watershed {uuid.uuid4().hex[:8]}",
            state="TEST",
            district="TEST",
            geometry_wkt=TEST_WKT,
        )
        watershed_id = watershed.id

        fetched = get_watershed_by_id(db, watershed_id)
        assert fetched is not None
        assert fetched.name == watershed.name

        area = get_watershed_area_sq_km(db, watershed_id)
        assert area is not None
        assert area > 0

        db.delete(fetched)
        db.commit()

def test_spatial_intersection():
    with SessionLocal() as db:
        watershed = create_watershed(
            db,
            name=f"Spatial Test {uuid.uuid4().hex[:8]}",
            state="TEST",
            district="TEST",
            geometry_wkt=TEST_WKT,
        )

        intersecting_wkt = (
            "MULTIPOLYGON (((76.9500 10.0500, "
            "76.9500 10.1500, "
            "77.0500 10.1500, "
            "77.0500 10.0500, "
            "76.9500 10.0500)))"
        )

        results = get_watersheds_intersecting_wkt(db, intersecting_wkt)
        assert any(item.id == watershed.id for item in results)

        db.delete(watershed)
        db.commit()
