# Design Prototypes

This document outlines the near-term prototyping plan that supports the MVP roadmap. It captures the goals for each prototype, the tools and fidelity targets, scheduled feedback checkpoints, and the key accessibility and performance KPIs each experience must demonstrate before engineering implementation begins. For broader context, see the [Product Roadmap](../docs/roadmap.md).

## Prototype Goals & Scope

### Sample Annotator Workspace
- **Objective:** Validate the reviewer experience for labeling batched samples with inline guidance and low-friction navigation.
- **Target fidelity:** High-fidelity interactive mockups with micro-interaction prototypes for autosave, undo, and keyboard navigation states.
- **Primary flows:** Batch intake overview, detailed sample annotation, consensus guidance surfaces, accessibility affordances (keyboard shortcuts, focus order, screen reader labels).
- **Design tools:** Figma for interactive flows, FigJam for annotator rubric mapping.

### Batch Worklist & Monitoring
- **Objective:** Demonstrate how operations leads triage batch readiness, review quality signals, and assign work to annotators.
- **Target fidelity:** High-fidelity dashboard prototype with clickable states for status filters, alert details, and assignment modals.
- **Primary flows:** Ingestion health overview, batch detail drill-in, assignment management, anomaly alert acknowledgement.
- **Design tools:** Figma for visual prototypes, Spreadsheet mock data for dashboard metrics exploration.

## Feedback & Review Sessions

| Session | Purpose | Date | Owner |
| --- | --- | --- | --- |
| Internal dry run | Walk through prototype flows with product and engineering leads to validate requirements coverage and interaction feasibility. | 2024-06-18 | Lead Product Designer |
| External pilot review | Test core tasks with two target annotators to capture usability issues before build. | 2024-06-25 | Research Lead |

## Accessibility & Performance KPIs

To align with the roadmap exit criteria, each prototype will be assessed against the following success metrics:

- **Keyboard accessibility coverage:** Keyboard shortcuts must cover at least 90% of annotator actions without error states, and focus order must remain consistent across workflow steps, mirroring the Sample Annotator milestone criteria.
- **Real-time feedback responsiveness:** Prototype interactions should demonstrate perceived autosave and update responses within five seconds to match the MVP collaboration performance target.
- **Guidance discoverability:** Consensus guidance, tooltips, and schema definitions must be reachable within two interactions from any annotation screen, ensuring onboarding support is embedded as called for in the roadmap.
- **Operational alerting latency:** Batch worklist surfaces anomaly alerts and data quality signals with a simulated reporting delay of under one hour, consistent with the ingestion milestone KPI.

Document owners should capture findings from each feedback session and note any gaps against these KPIs to keep the prototypes on track for MVP readiness.
