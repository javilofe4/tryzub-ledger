#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
cd backend
python -m pytest --maxfail=1 --disable-warnings -q
cd ../frontend
npm run lint
npm run typecheck
