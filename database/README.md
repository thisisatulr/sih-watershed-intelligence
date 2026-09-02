# Database / PostGIS Foundation

This module provides the Phase 1 database layer for the SIH Watershed Intelligence Platform.

## Stack

- PostgreSQL
- PostGIS
- SQLAlchemy 2.x
- GeoAlchemy2
- pytest

## Start PostgreSQL + PostGIS

Copy `.env.example` to `.env`, then:

```bash
docker compose up -d
```

Check the database:

```bash
docker compose ps
```

## Install Python dependencies

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then:

```bash
python -m pip install -r backend/requirements-db.txt
```

## Initialize and seed

```bash
python database/seed/seed.py
```

The seed creates **synthetic demo data only**. It is not official government watershed data.

## Test

```bash
pytest -q
```

Tests are intentionally non-destructive: temporary watershed rows are removed after the relevant tests.

## Schema

### `watersheds`

- `id` — UUID primary key
- `name`
- `state`
- `district`
- `area_sq_km`
- `geometry` — PostGIS `MULTIPOLYGON`, EPSG:4326
- `created_at`
- `updated_at`

### `layer_metadata`

- `id` — UUID primary key
- `name`
- `layer_type`
- `description`
- `source`
- `version`
- `metadata` — JSONB
- `created_at`

The SQLAlchemy attribute for the `metadata` column is `metadata_json` because `metadata` is reserved by SQLAlchemy's declarative API.

## Data-access interface

Use repositories instead of raw SQL in API routers:

```python
get_watershed_by_id(db, watershed_id)
get_watersheds(db)
get_watershed_area_sq_km(db, watershed_id)
get_watersheds_intersecting_wkt(db, geometry_wkt)

get_layers(db)
get_layers_by_type(db, "rainfall")
```

## CRS rule

Watershed geometries are stored canonically as EPSG:4326.

Metric calculations such as area use PostGIS `geography` conversion so the calculation is performed in metres rather than treating longitude/latitude degrees as planar units.

Incoming GIS data should be CRS-validated and transformed to EPSG:4326 before persistence.

## Stop database

```bash
docker compose down
```

To completely reset the development database and rerun initialization scripts:

```bash
docker compose down -v
docker compose up -d
```
