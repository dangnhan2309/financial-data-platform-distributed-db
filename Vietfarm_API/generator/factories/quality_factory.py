from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from api.models.quality_models import AloeQualityTest, QualityTestResult
from generator.config import SeedConfig
from generator.factories.common import add_days, make_id


@dataclass
class QualityEntities:
    quality_tests: list[AloeQualityTest]
    quality_test_results: list[QualityTestResult]


def build_quality_entities(
    config: SeedConfig,
    processing_batch_ids: list[str],
    test_item_ids: list[str],
) -> QualityEntities:
    quality_tests: list[AloeQualityTest] = []
    quality_test_results: list[QualityTestResult] = []

    for i in range(1, config.rows_per_table + 1):
        quality_test_id = make_id(config.run_tag, "QT", i)

        quality_tests.append(
            AloeQualityTest(
                quality_test_id=quality_test_id,
                processing_batch_id=processing_batch_ids[(
                    i - 1) % len(processing_batch_ids)],
                test_date=add_days(date(2026, 2, 1), i),
                inspector=f"Inspector {i}",
                result_status=["PASS", "FAIL", "PENDING"][(i - 1) % 3],
            )
        )

        quality_test_results.append(
            QualityTestResult(
                result_id=make_id(config.run_tag, "QTR", i),
                quality_test_id=quality_test_id,
                test_item_id=test_item_ids[(i - 1) % len(test_item_ids)],
                actual_value=Decimal("8") + Decimal((i - 1) % 8),
            )
        )

    return QualityEntities(
        quality_tests=quality_tests,
        quality_test_results=quality_test_results,
    )
