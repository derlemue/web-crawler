#!/bin/bash

# === Konfiguration ===
REPO_PATH="/root/stauffenberg_bot/"
BRANCH="master"
COMMIT_MESSAGE="🔄 Automatisches Update: $(date +'%Y-%m-%d %H:%M:%S')"

cd "$REPO_PATH" || {
  echo "❌ Fehler: Pfad $REPO_PATH nicht gefunden."
  exit 1
}

# === Check: Änderungen vorhanden? ===
if git diff --quiet && git diff --cached --quiet; then
  echo "🟢 Keine Änderungen – Push wird übersprungen."
  exit 0
fi

# === Git Push ===
echo "📤 Pushe Änderungen an $BRANCH..."
git add .
git commit -m "$COMMIT_MESSAGE"

## Pull mit Konfliktvermeidung
#git pull origin "$BRANCH" --rebase || {
#  echo "⚠️ Pull mit Rebase fehlgeschlagen!"
#  exit 1
#}

# Push
git push origin "$BRANCH" -f && echo "✅ Push abgeschlossen: $COMMIT_MESSAGE"
