from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from caqdashub.ingestion import SourceConfig, build_service


def write_sample(tmp_path: Path, source_id: str, payload: dict) -> Path:
    source_dir = tmp_path / source_id.replace(":", "_")
    source_dir.mkdir(parents=True, exist_ok=True)
    file_path = source_dir / "sample.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")
    return file_path


def test_ingestion_normalizes_reddit_payload(tmp_path: Path) -> None:
    payload = {
        "data": {
            "id": "abc123",
            "title": "Example post",
            "selftext": "Narrative content",
            "created_utc": 1_700_000_000,
            "permalink": "/r/example/comments/abc123/example_post/",
            "author": "sample_user",
            "score": 42,
            "subreddit": "example",
        }
    }
    write_sample(tmp_path, "reddit:example", payload)

    configs = [SourceConfig(source_id="reddit:example", glob="*.json")]
    service = build_service(configs, tmp_path, tmp_path / "out")
    stats = service.run_once()

    assert stats.processed == 1
    output_file = next((tmp_path / "out").glob("*.json"))
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["id"] == "abc123"
    assert data["source"] == "reddit:example"
    assert data["metadata"]["subreddit"] == "example"
    assert data["payload"]["text"].startswith("Narrative content")
    received_at = datetime.fromisoformat(data["received_at"])
    assert received_at.tzinfo is not None
    assert received_at.tzinfo.utcoffset(received_at) == timezone.utc.utcoffset(received_at)


def test_ingestion_records_failures(tmp_path: Path) -> None:
    payload = {"id": "missing_text"}
    write_sample(tmp_path, "reddit:broken", payload)

    configs = [SourceConfig(source_id="reddit:broken", glob="*.json")]
    service = build_service(configs, tmp_path, tmp_path / "out")
    stats = service.run_once()

    assert stats.processed == 0
    assert stats.failed == 1
    errors = list((tmp_path / "out" / "_errors").glob("*.log"))
    assert len(errors) == 1
