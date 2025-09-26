"""Command-line runner for the ingestion service."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from caqdashub.ingestion import SourceConfig, build_service


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize social media JSON payloads into Samples")
    parser.add_argument("input", type=Path, help="Directory containing source folders")
    parser.add_argument("output", type=Path, help="Directory to write normalized Sample JSON files")
    parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        help="Source identifier in the form source_id=glob (e.g. reddit:askreddit=*.json)",
    )
    return parser.parse_args()


def build_configs(args: argparse.Namespace) -> List[SourceConfig]:
    configs: List[SourceConfig] = []
    if not args.sources:
        raise SystemExit("At least one --source must be provided")
    for spec in args.sources:
        try:
            source_id, glob = spec.split("=", 1)
        except ValueError as exc:
            raise SystemExit("Sources must be in the form source_id=glob") from exc
        try:
            configs.append(SourceConfig(source_id=source_id.strip(), glob=glob.strip()))
        except ValueError as exc:
            raise SystemExit(str(exc))
    return configs


def main() -> None:
    args = parse_args()
    configs = build_configs(args)
    service = build_service(configs=configs, input_base=args.input, output_dir=args.output)
    stats = service.run_once()
    print(f"Processed {stats.processed} samples (failed: {stats.failed})")


if __name__ == "__main__":
    main()
