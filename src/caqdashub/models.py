"""Domain models that mirror the documented JSON schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class Attachment:
    uri: str
    content_type: str
    checksum: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {"uri": self.uri, "content_type": self.content_type}
        if self.checksum is not None:
            data["checksum"] = self.checksum
        return data


@dataclass
class SamplePayload:
    text: str
    attachments: Optional[List[Attachment]] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"text": self.text}
        if self.attachments:
            data["attachments"] = [attachment.to_dict() for attachment in self.attachments]
        return data


@dataclass
class Sample:
    id: str
    source: str
    received_at: datetime
    payload: SamplePayload
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "source": self.source,
            "received_at": self.received_at.isoformat(),
            "payload": self.payload.to_dict(),
            "metadata": self.metadata,
        }
        return data


@dataclass
class AnnotationLabel:
    feature: str
    value: Any
    start: Optional[int] = None
    end: Optional[int] = None

    def __post_init__(self) -> None:
        if (self.start is None) ^ (self.end is None):
            raise ValueError("start and end must both be provided when using evidence spans")
        if self.start is not None and self.end is not None and self.start > self.end:
            raise ValueError("start must be <= end")


@dataclass
class Annotation:
    id: str
    sample_id: str
    reviewer_id: str
    labels: Sequence[AnnotationLabel]
    status: str = "in_progress"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None


@dataclass
class ConsensusConflict:
    feature: str
    annotation_ids: List[str]
    status: str = "open"


@dataclass
class ConsensusFeature:
    name: str
    value: Any
    confidence: Optional[float] = None


@dataclass
class ConsensusDecision:
    id: str
    sample_id: str
    strategy: str
    features: List[ConsensusFeature]
    confidence: Optional[float] = None
    conflicts: List[ConsensusConflict] = field(default_factory=list)
    computed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AuditActor:
    type: str
    id: str


@dataclass
class AuditEntity:
    type: str
    id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditChange:
    field: str
    previous: Optional[Any] = None
    current: Optional[Any] = None


@dataclass
class AuditLog:
    id: str
    actor: AuditActor
    action: str
    entity: AuditEntity
    occurred_at: datetime
    changes: List[AuditChange] = field(default_factory=list)
    correlation_id: Optional[str] = None


def validate_sample(sample: Sample) -> None:
    if not sample.id:
        raise ValueError("sample.id is required")
    if not sample.source:
        raise ValueError("sample.source is required")
    if sample.received_at.tzinfo is None:
        raise ValueError("sample.received_at must be timezone-aware")
    if not sample.payload.text.strip():
        raise ValueError("sample.payload.text must not be blank")


__all__ = [
    "Attachment",
    "SamplePayload",
    "Sample",
    "AnnotationLabel",
    "Annotation",
    "ConsensusConflict",
    "ConsensusFeature",
    "ConsensusDecision",
    "AuditActor",
    "AuditEntity",
    "AuditChange",
    "AuditLog",
    "validate_sample",
]
