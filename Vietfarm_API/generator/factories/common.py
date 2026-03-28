from __future__ import annotations

from datetime import date, datetime, timedelta


def make_id(tag: str, prefix: str, index: int) -> str:
    return f"G{tag}_{prefix}_{index:04d}"


def add_days(base: date, days: int) -> date:
    return base + timedelta(days=days)


def add_hours(base: datetime, hours: int) -> datetime:
    return base + timedelta(hours=hours)
