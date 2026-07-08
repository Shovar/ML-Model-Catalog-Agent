import uuid

from sqlalchemy import Column, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    version = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    owner_team = Column(String, nullable=False)
    status = Column(String, nullable=False)
    last_deployed_at = Column(String, nullable=False)
    cost_per_month_usd = Column(Float, nullable=False)
    kpi_supported = Column(String, nullable=False)
    notes = Column(String, nullable=False)

    metric_snapshots = relationship("MetricSnapshot", back_populates="model", cascade="all, delete-orphan")


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_id = Column(String, ForeignKey("models.id"), nullable=False)
    captured_at = Column(String, nullable=False)
    latency_p95_ms = Column(Float, nullable=False)
    drift_score = Column(Float, nullable=False)
    accuracy_score = Column(Float, nullable=False)
    availability_pct = Column(Float, nullable=False)

    model = relationship("Model", back_populates="metric_snapshots")


def get_engine(db_url="sqlite:///catalogue.db"):
    return create_engine(db_url, echo=False)


def init_db(engine=None):
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(engine)
    return engine
