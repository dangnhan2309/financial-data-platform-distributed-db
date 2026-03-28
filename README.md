# Financial Data Platform Distributed DB

Distributed database project with a Vietfarm backend for aloe supply-chain operations, built with FastAPI, SQLAlchemy, and Oracle.

## Completed Work

- Built Vietfarm FastAPI backend with layered structure: models, schemas, repositories, services, routers.
- Added Oracle DB utilities and session wiring for API and generator.
- Added modular sample-data generator with clean architecture:
	- `config`, `db`, `factories`, `validators`, `pipelines`, `runners`
- Implemented seed flow to insert dependency-safe data across master/farming/processing/quality/production tables.
- Implemented cleanup flow by run tag to quickly delete generated test data.
- Verified seed and cleanup directly on Oracle database.
- Verified generated data through API endpoints (Swagger-backed routes).

## Repository Layout

- `Vietfarm_API/api`
	- `models`: SQLAlchemy entities grouped by business domain
	- `schemas`: request/response contracts
	- `repositories`: data access layer
	- `services`: business logic layer
	- `routers`: API endpoints
	- `utils`: Oracle connection and DB session configuration
- `Vietfarm_API/generator`
	- `config`: seed configuration model
	- `db`: database helper functions
	- `factories`: data builders for each business domain
	- `validators`: preflight checks before seeding
	- `pipelines`: orchestration flow for end-to-end data generation
	- `runners`: CLI entrypoints

## Prerequisites

- Python 3.10+
- Oracle database reachable from local environment
- Virtual environment at `.venv`

## Oracle Configuration

Current configuration is loaded from:

- `Vietfarm_API/api/utils/oracle_settings.py`

Environment variables:

- `ORACLE_USER`
- `ORACLE_PASSWORD`
- `ORACLE_HOST`
- `ORACLE_PORT`
- `ORACLE_SERVICE`
- `ORACLE_SQL_ECHO`

## Run Backend API

From `Vietfarm_API`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8011 --reload
```

Run without reload:

```powershell
..\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8011
```

Swagger UI:

- `http://127.0.0.1:8011/docs`

Shortcut script:

```powershell
.\Script_activate_api.bat
```

## Generate Sample Data

The generator follows a clean architecture flow:

1. Validate required tables
2. Build master data
3. Build farming data
4. Build processing data
5. Build quality data
6. Build production and dispatch data

Each table receives approximately the same number of rows (default: 100).

From `Vietfarm_API`:

```powershell
..\.venv\Scripts\python.exe -m generator.runners.run_seed --rows 100 --tag AUTO100
```

Alternative entrypoint:

```powershell
..\.venv\Scripts\python.exe -m generator.seed_data --rows 100
```

Cleanup by run tag (delete generated rows quickly):

```powershell
..\.venv\Scripts\python.exe -m generator.runners.cleanup_seed --tag AUTO100
```

Optional arguments:

- `--rows`: rows per table
- `--seed`: deterministic random seed
- `--tag`: custom run tag for generated IDs

Example:

```powershell
..\.venv\Scripts\python.exe -m generator.runners.run_seed --rows 100 --seed 20260328 --tag DEMO01
```

## Test Guide

### 1. Seed Test Data

From `Vietfarm_API`:

```powershell
..\.venv\Scripts\python.exe -m generator.runners.run_seed --rows 100 --tag AUTO100
```

Expected: command prints `[OK] Seed completed` and table counts.

### 2. Validate in Oracle SQL Developer

Quick count checks:

```sql
SELECT COUNT(*) AS aloefarm_cnt FROM aloefarm WHERE farm_id LIKE 'GAUTO100_%';
SELECT COUNT(*) AS factory_cnt FROM factory WHERE factory_id LIKE 'GAUTO100_%';
SELECT COUNT(*) AS qtr_cnt FROM qualitytestresult WHERE result_id LIKE 'GAUTO100_%';
```

Sample rows:

```sql
SELECT * FROM aloefarm
WHERE farm_id LIKE 'GAUTO100_%'
ORDER BY farm_id
FETCH FIRST 10 ROWS ONLY;

SELECT result_id, quality_test_id, test_item_id, actual_value
FROM qualitytestresult
WHERE result_id LIKE 'GAUTO100_%'
ORDER BY result_id
FETCH FIRST 20 ROWS ONLY;
```

### 3. Validate in Swagger

Start API, then open:

- `http://127.0.0.1:8011/docs`

Test these GET endpoints:

- `/master-data/aloe-farms/GAUTO100_FARM_0001`
- `/master-data/factories/GAUTO100_FAC_0001`
- `/master-data/machines/GAUTO100_MAC_0001`
- `/master-data/aloe-farms?offset=0&limit=5`

### 4. Cleanup and Re-test Loop

```powershell
..\.venv\Scripts\python.exe -m generator.runners.cleanup_seed --tag AUTO100
..\.venv\Scripts\python.exe -m generator.runners.run_seed --rows 100 --tag AUTO100
```

After cleanup, expected count:

```sql
SELECT COUNT(*) AS cnt_after_cleanup FROM aloefarm WHERE farm_id LIKE 'GAUTO100_%';
```

Expected value: `0` before re-seeding.

## Notes

- Generator skips insertion into `fermentationlog` when the table does not exist.
- IDs are namespaced by run tag to reduce collision risk.
- For production use, avoid storing database passwords directly in source code.
