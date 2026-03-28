from __future__ import annotations

import argparse

from generator.config import build_seed_config
from generator.pipelines.seed_pipeline import run_seed_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seed Vietfarm sample data")
    parser.add_argument("--rows", type=int, default=100, help="Rows per table")
    parser.add_argument("--seed", type=int,
                        default=20260328, help="Random seed")
    parser.add_argument("--tag", type=str, default=None,
                        help="Optional run tag")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = build_seed_config(
        rows_per_table=args.rows,
        random_seed=args.seed,
        run_tag=args.tag,
    )

    summary = run_seed_pipeline(config)

    print("[OK] Seed completed")
    print(f"run_tag={summary.run_tag}")
    print(f"rows_per_table={summary.rows_per_table}")
    print(f"fermentation_enabled={summary.fermentation_enabled}")
    for table_name in sorted(summary.inserted_tables):
        print(f"{table_name}: {summary.inserted_tables[table_name]}")


if __name__ == "__main__":
    main()
