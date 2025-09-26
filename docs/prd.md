# Product Requirements Document

The MVP baseline defined in the [Product Roadmap](roadmap.md) establishes the scope that engineering, design, and research will deliver for launch.

## Problem Statement
Qualitative research teams struggle to turn large volumes of social media narratives into reliable, auditable insights. Manual collection, ad hoc spreadsheets, and inconsistent annotation practices slow analysis and introduce compliance risk.

## MVP Solution Overview
- Provide ingestion tooling that normalizes Reddit and forum exports into a governed `Sample` schema with connector metadata.
- Equip operations leads with batch triage dashboards that surface ingest health, assignment status, and data quality alerts.
- Deliver an accessible Sample Annotator workspace with schema guidance, autosave/undo, and consensus cues so reviewers stay aligned.
- Automate consensus scoring and export packaging to deliver structured features and conflicts to downstream consumers with traceable lineage.
- Record audit trails and operational metrics covering ingestion through export to support compliance and on-call workflows.

## Success Metrics
- 95% of daily social media payloads process automatically into normalized samples without manual remediation.
- Annotator throughput reaches the planned target (e.g., 25 samples/hour) while maintaining inter-rater agreement above the roadmap threshold.
- Consensus jobs complete within the agreed SLA and deliver exports with verified checksums and delivery receipts.
- Operations leads resolve ingest anomalies within one business hour using the provided dashboards and alerts.

## Out of Scope (Post-MVP)
The initiatives listed as stretch goals in the [Product Roadmap](roadmap.md#post-mvp-stretch-goals) remain outside the launch commitment and will be reprioritized once the MVP is stable.

## Dependencies & Risks
- Finalizing identity provider integration and reviewer access provisioning.
- Confirming schema registry strategy and downstream integration requirements for the export payloads.
- Coordinating with compliance and security teams on PII redaction, storage policies, and audit retention timelines.
