from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SeedConfig:
    rows_per_table: int = 100
    random_seed: int = 20260328
    run_tag: str = ""


def build_seed_config(rows_per_table: int, random_seed: int, run_tag: str | None = None) -> SeedConfig:
    if rows_per_table <= 0:
        raise ValueError("rows_per_table must be > 0")

    resolved_tag = run_tag or datetime.now().strftime("%y%m%d%H%M%S")
    return SeedConfig(
        rows_per_table=rows_per_table,
        random_seed=random_seed,
        run_tag=resolved_tag,
    )
