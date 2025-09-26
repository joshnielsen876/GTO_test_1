# GTO_test_1
We’re building an environment that lets humans and AI work together to turn scattered narratives into structured features. Humans discover and agree on features in small batches, then AI scales that schema to the rest of the data.

## Planning Docs
- [Product Roadmap](docs/roadmap.md)
- [Product Requirements Document](docs/prd.md)
- [Architecture Overview](docs/architecture/overview.md)
- [Data Model Schemas](docs/architecture/data-model.md)
- [Implementation Plan](docs/implementation-plan.md)

## Getting Started

### Normalize social media payloads locally

1. Place exported Reddit or forum JSON payloads under an input directory grouped by logical source (e.g., `data/incoming/reddit:askreddit/`).
2. Run the ingestion script to normalize posts into the shared `Sample` format:

   ```bash
   PYTHONPATH=src python scripts/run_ingestion.py data/incoming data/normalized --source "reddit:askreddit=*.json"
   ```

3. Normalized samples will appear in the output directory as JSON files ready for batching.

### Run tests

```bash
PYTHONPATH=src pytest
```
