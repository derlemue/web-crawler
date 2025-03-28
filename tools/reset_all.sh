#!/bin/bash

# Setze Basisverzeichnis relativ zum Skriptstandort
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

DB_PATH="$BASE_DIR/data/database.db"
SCREENSHOT_DIR="$BASE_DIR/data/screenshots"
LOG_DIR="$BASE_DIR/data/logs"

echo "⚠️  Achtung: Dieser Vorgang löscht alle gespeicherten Daten!"
read -p "❓ Bist du sicher? (ja/nein): " confirm

if [[ "$confirm" != "ja" ]]; then
  echo "❌ Vorgang abgebrochen."
  exit 1
fi

echo "🧹 Datenbank löschen ..."
rm -f "$DB_PATH"

echo "🧼 Screenshots löschen ..."
rm -rf "$SCREENSHOT_DIR"
mkdir -p "$SCREENSHOT_DIR"

echo "🗑️ Logs löschen ..."
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"

echo "📦 Docker Volumes und Container entfernen ..."
cd "$BASE_DIR" || exit 1
docker-compose down --volumes

echo "✅ Zurückgesetzt. Starte nun neu mit:"
echo "   docker-compose up -d --build --remove-orphans"
