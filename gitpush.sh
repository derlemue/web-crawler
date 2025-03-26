#!/bin/bash

# Konfiguration
REPO_PATH="/root/stauffenberg_bot/"
BRANCH="main"
COMMIT_MESSAGE="Automatisches Update: $(date +'%Y-%m-%d %H:%M:%S')"

cd "$REPO_PATH" || exit 1

# Git-Prozess
git add .
git commit -m "$COMMIT_MESSAGE"
git pull origin "$BRANCH" --rebase
git push origin "$BRANCH"

echo "Push abgeschlossen am $(date)"
