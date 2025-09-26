"""Ingestion service components for social narrative data."""

from .service import IngestionService, build_service
from .sources import LocalJsonSource, SourceConfig

__all__ = ["IngestionService", "LocalJsonSource", "SourceConfig", "build_service"]
