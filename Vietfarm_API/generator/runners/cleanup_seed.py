from __future__ import annotations

import argparse

from generator.pipelines.cleanup_pipeline import run_cleanup_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cleanup seeded Vietfarm sample data by run tag")
    parser.add_argument("--tag", type=str, required=True,
                        help="Run tag used in seed command, for example AUTO100")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    summary = run_cleanup_pipeline(args.tag)

    print("[OK] Cleanup completed")
    print(f"run_tag={summary.run_tag}")
    for table_name in sorted(summary.deleted_tables):
        print(f"{table_name}: {summary.deleted_tables[table_name]}")


if __name__ == "__main__":
    main()
