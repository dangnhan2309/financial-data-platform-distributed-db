from sqlalchemy import Column, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from api.utils.database import Base


class AloeQualityTest(Base):
    __tablename__ = "aloequalitytest"

    quality_test_id = Column("quality_test_id", String(50), primary_key=True)
    processing_batch_id = Column(
        "processing_batch_id", String(50), ForeignKey("aloeprocessingbatch.processing_batch_id"), nullable=False
    )
    test_date = Column("test_date", Date, nullable=False)
    inspector = Column("inspector", String(100))
    result_status = Column("result_status", String(50))

    processing_batch = relationship(
        "AloeProcessingBatch", back_populates="quality_tests")
    test_results = relationship(
        "QualityTestResult", back_populates="quality_test")


class QualityTestResult(Base):
    __tablename__ = "qualitytestresult"

    result_id = Column("result_id", String(50), primary_key=True)
    quality_test_id = Column(
        "quality_test_id", String(50), ForeignKey("aloequalitytest.quality_test_id"), nullable=False
    )
    test_item_id = Column("test_item_id", String(50), ForeignKey(
        "qualitytestitem.test_item_id"), nullable=False)
    actual_value = Column("actual_value", Numeric(10, 2))

    quality_test = relationship(
        "AloeQualityTest", back_populates="test_results")
    test_item = relationship(
        "QualityTestItem", back_populates="quality_test_results")
