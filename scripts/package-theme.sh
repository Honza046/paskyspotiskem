#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"
ZIP="$OUT/paskyonline.zip"
THEME="paskyonline"

mkdir -p "$OUT"
rm -f "$ZIP"

cd "$ROOT"
zip -r "$ZIP" . \
  -x "./dist/*" \
  -x "./.git/*" \
  -x "./node_modules/*" \
  -x "./index.html" \
  -x "./sortiment.html" \
  -x "./galerie.html" \
  -x "./sortiment/*" \
  -x "./preview.html" \
  -x "./docker-compose.yml" \
  -x "./package.json" \
  -x "./package-lock.json" \
  -x "./scripts/*" \
  -x "./*.zip"

echo ""
echo "Hotovo: $ZIP"
echo "Nahrajte v WordPressu: Vzhled → Šablony → Přidat novou → Nahrát šablonu"
