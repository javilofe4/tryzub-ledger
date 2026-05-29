#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
cd backend
python -m pytest
