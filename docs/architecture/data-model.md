# Data Model

This document outlines the JSON payloads that power ingestion, annotation, and export flows in the MVP. Schemas follow JSON Sche
ma draft-07 conventions and may be expressed as OpenAPI components for service implementations.

## Sample
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Sample",
  "type": "object",
  "required": ["id", "source", "received_at", "payload"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "source": { "type": "string", "description": "Originating connector identifier" },
    "received_at": { "type": "string", "format": "date-time" },
    "metadata": { "type": "object", "additionalProperties": true, "description": "Connector context (e.g., subreddit, author handle, language)" },
    "payload": {
      "type": "object",
      "required": ["text"],
      "properties": {
        "text": { "type": "string" },
        "attachments": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["uri", "content_type"],
            "properties": {
              "uri": { "type": "string", "format": "uri" },
              "content_type": { "type": "string" },
              "checksum": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

## Feature
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Feature",
  "type": "object",
  "required": ["name", "value", "confidence"],
  "properties": {
    "name": { "type": "string" },
    "value": { "type": ["string", "number", "boolean", "null", "object", "array"] },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "source_annotation_ids": {
      "type": "array",
      "items": { "type": "string", "format": "uuid" }
    },
    "derived": { "type": "boolean", "default": false }
  }
}
```

## Annotation
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Annotation",
  "type": "object",
  "required": ["id", "sample_id", "reviewer_id", "labels", "created_at"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "sample_id": { "type": "string", "format": "uuid" },
    "reviewer_id": { "type": "string" },
    "labels": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["feature", "value"],
        "properties": {
          "feature": { "type": "string" },
          "value": { "type": ["string", "number", "boolean", "null", "object", "array"] },
          "evidence_span": {
            "type": "object",
            "required": ["start", "end"],
            "properties": {
              "start": { "type": "integer", "minimum": 0 },
              "end": { "type": "integer", "minimum": 0 }
            }
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["in_progress", "submitted", "needs_review"],
      "default": "in_progress"
    },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  }
}
```

## ConsensusDecision
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ConsensusDecision",
  "type": "object",
  "required": ["id", "sample_id", "strategy", "features", "computed_at"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "sample_id": { "type": "string", "format": "uuid" },
    "strategy": { "type": "string", "enum": ["majority_vote", "weighted_vote", "adjudicated"] },
    "features": {
      "type": "array",
      "items": { "$ref": "#/definitions/Feature" }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "conflicts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["feature", "annotation_ids"],
        "properties": {
          "feature": { "type": "string" },
          "annotation_ids": {
            "type": "array",
            "items": { "type": "string", "format": "uuid" }
          },
          "status": { "type": "string", "enum": ["open", "resolved"] }
        }
      }
    },
    "computed_at": { "type": "string", "format": "date-time" }
  },
  "definitions": {
    "Feature": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "ConsensusFeature",
      "type": "object",
      "required": ["name", "value"],
      "properties": {
        "name": { "type": "string" },
        "value": { "type": ["string", "number", "boolean", "null", "object", "array"] },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

## AuditLog
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AuditLog",
  "type": "object",
  "required": ["id", "actor", "action", "entity", "occurred_at"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "actor": {
      "type": "object",
      "required": ["type", "id"],
      "properties": {
        "type": { "type": "string", "enum": ["user", "service"] },
        "id": { "type": "string" }
      }
    },
    "action": { "type": "string" },
    "entity": {
      "type": "object",
      "required": ["type", "id"],
      "properties": {
        "type": { "type": "string" },
        "id": { "type": "string" },
        "metadata": { "type": "object", "additionalProperties": true }
      }
    },
    "changes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["field"],
        "properties": {
          "field": { "type": "string" },
          "previous": {},
          "current": {}
        }
      }
    },
    "occurred_at": { "type": "string", "format": "date-time" },
    "correlation_id": { "type": "string" }
  }
}
```

## Open Questions & Assumptions
- **Schema registry**: Need to decide whether to host schemas in a central registry or version them with service code.
- **Backward compatibility**: Assume additive-only schema changes during MVP; evaluate migration tooling for breaking updates.
- **Redaction fields**: Identify which sample and annotation fields require encryption or hashing at rest.
- **Feature extensibility**: Confirm whether derived features must include lineage metadata beyond annotation IDs.
