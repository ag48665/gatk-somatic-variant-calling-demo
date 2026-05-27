#!/usr/bin/env bash
set -euo pipefail
CONFIG=${1:-config/example_config.yaml}
python -m somatic_pipeline.cli run --config "$CONFIG" --dry-run
