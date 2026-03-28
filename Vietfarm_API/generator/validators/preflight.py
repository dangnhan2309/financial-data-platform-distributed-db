from __future__ import annotations

from generator.db import has_table


REQUIRED_TABLES = [
    "aloefarm",
    "warehouse",
    "factory",
    "steptype",
    "machine",
    "operator",
    "qualitytestitem",
    "packagingline",
    "transportvehicle",
    "aloefield",
    "aloeplantingbatch",
    "aloeharvestbatch",
    "rawmaterialreceiving",
    "rawmaterialinspection",
    "aloeprocessingbatch",
    "machinemaintenance",
    "processingmaterialusage",
    "processingstep",
    "processingoperator",
    "aloequalitytest",
    "qualitytestresult",
    "aloeproductionlot",
    "packagingbatch",
    "inventory",
    "dispatchorder",
    "dispatchvehicle",
]


def ensure_required_tables() -> None:
    missing = [table for table in REQUIRED_TABLES if not has_table(table)]
    if missing:
        joined = ", ".join(sorted(missing))
        raise RuntimeError(f"Missing required tables: {joined}")
