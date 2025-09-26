"""Source connectors for ingesting narrative social media content."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Iterator

from ..models import Sample, SamplePayload


@dataclass
class SourceConfig:
    """Configuration shared by ingestion source connectors."""

    source_id: str
    glob: str = "*.json"

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id is required")
        if not self.glob:
            raise ValueError("glob pattern is required")


@dataclass
class LocalJsonSource:
    """Reads JSON payloads representing social media posts from a directory."""

    config: SourceConfig
    path: Path

    def iter_samples(self) -> Iterator[Sample]:
        for file_path in sorted(self.path.glob(self.config.glob)):
            if not file_path.is_file():
                continue
            with file_path.open("r", encoding="utf-8") as handle:
                try:
                    payload = json.load(handle)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{file_path} is not valid JSON: {exc}") from exc

            yield self._map_payload(payload)

    def _map_payload(self, payload: Dict[str, object]) -> Sample:
        post = payload.get("data", payload)
        text = self._extract_text(post)
        sample_payload = SamplePayload(text=text)
        received_at = self._parse_timestamp(post)
        metadata = {
            "permalink": post.get("permalink"),
            "author": post.get("author"),
            "score": post.get("score"),
            "subreddit": post.get("subreddit"),
        }
        sample_id = str(post.get("id") or post.get("name") or "")
        if not sample_id:
            raise ValueError("Post payload missing identifier")
        return Sample(
            id=sample_id,
            source=self.config.source_id,
            received_at=received_at,
            payload=sample_payload,
            metadata={k: v for k, v in metadata.items() if v is not None},
        )

    @staticmethod
    def _extract_text(post: Dict[str, object]) -> str:
        body_fields = [
            post.get("selftext"),
            post.get("title"),
            post.get("body"),
            post.get("text"),
        ]
        text_fragments = [str(value).strip() for value in body_fields if isinstance(value, str) and value.strip()]
        text = "\n\n".join(text_fragments)
        if not text:
            raise ValueError("Post payload does not contain text-like fields")
        return text

    def _parse_timestamp(self, post: Dict[str, object]) -> datetime:
        raw = post.get("created_utc") or post.get("created_at")
        if isinstance(raw, (int, float)):
            return datetime.fromtimestamp(float(raw), tz=timezone.utc)
        if isinstance(raw, str):
            try:
                return datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"Could not parse timestamp '{raw}'") from exc
        return datetime.now(tz=timezone.utc)


def iter_sources(configs: Iterable[SourceConfig], base_path: Path) -> Iterator[LocalJsonSource]:
    for config in configs:
        yield LocalJsonSource(config=config, path=base_path / config.source_id.replace(":", "_"))
