"""Ingestion service that normalizes social media posts into Samples."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, List

from ..models import Sample, validate_sample
from .sources import LocalJsonSource, SourceConfig


@dataclass
class IngestionStats:
    processed: int = 0
    failed: int = 0


@dataclass
class IngestionService:
    """Coordinates ingestion sources and persists normalized samples."""

    sources: Iterable[LocalJsonSource]
    output_dir: Path

    def run_once(self) -> IngestionStats:
        stats = IngestionStats()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for source in self.sources:
            for sample in self._safe_iter_samples(source, stats):
                self._persist_sample(sample)
        return stats

    def _safe_iter_samples(self, source: LocalJsonSource, stats: IngestionStats) -> Iterator[Sample]:
        iterator = source.iter_samples()
        while True:
            try:
                sample = next(iterator)
            except StopIteration:
                break
            except ValueError as exc:
                stats.failed += 1
                self._write_error(source, exc)
                continue

            try:
                validate_sample(sample)
            except ValueError as exc:
                stats.failed += 1
                self._write_error(source, exc)
                continue

            stats.processed += 1
            yield sample

    def _persist_sample(self, sample: Sample) -> None:
        target = self.output_dir / f"{sample.id or self._timestamp_id()}.json"
        payload = sample.to_dict()
        with target.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    def _write_error(self, source: LocalJsonSource, exc: Exception) -> None:
        error_dir = self.output_dir / "_errors"
        error_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        error_file = error_dir / f"{source.config.source_id}-{timestamp}.log"
        error_file.write_text(str(exc), encoding="utf-8")

    @staticmethod
    def _timestamp_id() -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")


def build_service(configs: Iterable[SourceConfig], input_base: Path, output_dir: Path) -> IngestionService:
    sources: List[LocalJsonSource] = [LocalJsonSource(config=c, path=input_base / c.source_id.replace(":", "_")) for c in configs]
    return IngestionService(sources=sources, output_dir=output_dir)
