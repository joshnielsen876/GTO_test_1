# Product Roadmap

This roadmap outlines the current minimum viable product (MVP) scope, how success will be evaluated, and the initiatives that are intentionally deferred until after the initial launch. For detailed product context, see the [Product Requirements Document](prd.md).

## Current MVP Scope
- **Social narrative ingestion**: Normalize Reddit, forum, and long-form narrative payloads into validated samples with traceable metadata.
- **Batch management & triage**: Give operations leads visibility into ingest health, batch readiness, and assignment flows so work stays balanced.
- **Reviewer annotation workspace**: Provide accessible labeling tools with schema guidance, autosave, undo, and keyboard coverage for high-throughput reviewers.
- **Consensus & export automation**: Compute agreement scores, surface conflicts, and deliver structured features to downstream partners with audit trails.
- **Operational observability**: Capture audit logs, data quality metrics, and delivery receipts so compliance and support teams can diagnose issues quickly.

## Acceptance Criteria
- Ingestion jobs process the daily social narrative feeds without manual retries and attach source metadata for every sample.
- Operations leads can assign, reprioritize, and monitor batches from the worklist with latency under one minute from ingest to visibility.
- Reviewers complete batches with autosave feedback under five seconds and 90% keyboard coverage for high-frequency actions.
- Consensus runs close within the agreed service-level window, emitting conflict queues and export-ready feature payloads.
- Monitoring and audit logs capture end-to-end traceability for samples, annotations, and exports with on-call runbooks documented.

## Milestones

### Data ingestion & batching
**Objective:** Establish a resilient pipeline that normalizes raw social media narratives into review-ready batches for the workspace.

**Exit Criteria**
- Source connectors handle daily social feed exports without manual retries.
- Batching rules group samples into reviewer-sized sets with audit trails.
- Data quality reports flag anomalies to the research team within an hour of ingestion.

**Planned Epics / Issues**
- [Backend] Epic: Stream ingestion service with retryable jobs.
- [Research] Epic: Define sampling heuristics and quality thresholds.
- [Frontend] Issue: Batch readiness dashboard for operations leads.

Tracked on [MVP Delivery Board – Data ingestion & batching](https://github.com/orgs/gto-test/projects/1/views/1?filter=Milestone%3A%22Data%20ingestion%20%26%20batching%22).

### Sample annotator
**Objective:** Deliver an intuitive annotation workspace that lets reviewers label batched samples consistently and efficiently.

**Exit Criteria**
- Reviewers can progress through assigned batches with autosave and undo support.
- Consensus guidance and tooltips surface schema definitions inline during labeling.
- Keyboard shortcuts cover the top 90% of annotator actions without errors.

**Planned Epics / Issues**
- [Frontend] Epic: Interactive annotation interface with accessibility baseline.
- [Backend] Epic: Annotation persistence API with optimistic locking.
- [Research] Issue: Labeling rubric and reviewer training content.

Tracked on [MVP Delivery Board – Sample annotator](https://github.com/orgs/gto-test/projects/1/views/1?filter=Milestone%3A%22Sample%20annotator%22).

### Consensus & export
**Objective:** Automate consensus scoring and export flows so downstream teams receive high-confidence structured features.

**Exit Criteria**
- Consensus calculations run on schedule and surface conflicts for manual review.
- Exports deliver structured data to target systems with checksum verification.
- Stakeholders receive notifications when exports succeed or require action.

**Planned Epics / Issues**
- [Backend] Epic: Consensus engine with configurable agreement thresholds.
- [Frontend] Issue: Conflict resolution UI for reviewer leads.
- [Research] Epic: Evaluation benchmarks validating consensus accuracy.

Tracked on [MVP Delivery Board – Consensus & export](https://github.com/orgs/gto-test/projects/1/views/1?filter=Milestone%3A%22Consensus%20%26%20export%22).

## Post-MVP Stretch Goals
- Advanced analytics dashboards highlighting workspace trends over time.
- Automation hooks for third-party integrations (e.g., Slack notifications, task sync).
- Granular audit logging that supports export and compliance workflows.
- In-product onboarding tours personalized to user roles.
