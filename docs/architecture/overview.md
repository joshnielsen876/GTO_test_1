# Architecture Overview

This overview captures the proposed service boundaries, storage selections, and integrations supporting the MVP workflow descri
bed in the roadmap. It establishes a baseline for further design discussions and highlights assumptions that require follow-up.

## Service Boundaries

### Ingestion Service
- Continuously polls social narrative sources (Reddit exports, community forums, secure SFTP drops) and normalizes payloads into the internal JSON
  sample schema.
- Performs lightweight validation (schema, safety filters) before enqueueing batches for annotation.
- Publishes ingest events to the message broker so downstream services can react to new samples.

### Annotation API
- Provides authenticated REST and WebSocket endpoints that back the reviewer workspace.
- Manages assignment, optimistic locking, and persistence of annotations.
- Generates task metadata for the consensus worker based on reviewer submissions.

### Consensus Worker
- Listens to annotation-complete events and computes agreement scores across reviewers.
- Applies configured consensus strategies (majority vote, weighted experts) and persists decisions.
- Emits conflicts requiring manual review to the Annotation API for surfacing in the UI.

### Export Service
- Packages consensus outputs and derived features into partner-specific payloads (CSV, JSONL, warehouse loads).
- Handles delivery logistics, including retries, checksum validation, and notification webhooks.
- Maintains delivery receipts that feed the audit log and downstream billing.

## Storage Choices
- **Primary database:** PostgreSQL for transactional data (samples, annotations, consensus decisions) with row-level security.
- **Blob storage:** Encrypted S3 buckets for raw social media payloads and large attachments.
- **Message broker:** AWS SQS or Google Pub/Sub (TBD) for decoupling ingestion, annotation, and consensus workflows.
- **Caching:** Redis for session tokens, assignment queues, and rate limiting.
- **Analytics warehouse:** Snowflake / BigQuery (TBD) fed by scheduled exports for operational dashboards.

## Integration Points
- **Authentication provider:** Integrate with the identity service chosen by the platform team (Okta/Auth0 under evaluation).
- **Product analytics:** Emit structured events to Segment to capture reviewer efficiency metrics.
- **Support tooling:** Push audit log summaries to the internal ticketing system for compliance reporting.
- **Project tracker:** Sync milestone progress with the MVP Delivery Board for consistent status reporting.

## Open Questions & Assumptions
- **Authentication**: Assume SSO via SAML/OIDC is available; need confirmation on provider choice and provisioning flow.
- **Lock management**: Optimistic locking is assumed sufficient; evaluate the need for distributed locks under high concurrency.
- **PII handling**: Expect social media narratives to contain personal data; confirm data classification requirements and redaction approach.
- **Multi-region support**: MVP targets a single region; assess replication needs for disaster recovery post-MVP.
- **Message broker**: Decision between SQS and Pub/Sub pending infrastructure standards review.
