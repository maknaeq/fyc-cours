#!/usr/bin/env bash
# Installe le hook git de pre-commit (lint des règles de rédaction).
# À lancer une fois après le clonage, quel que soit l'outil utilisé (Claude Code,
# Codex, éditeur seul).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ln -sf ../../scripts/git-hooks/pre-commit "$ROOT/.git/hooks/pre-commit"
chmod +x "$ROOT/scripts/git-hooks/pre-commit"
echo "Hook pre-commit installé."
