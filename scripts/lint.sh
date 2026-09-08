#!/usr/bin/env bash
# Vérifie les règles de rédaction mécanisables (charte/regles-redaction.md).
#
# Usage :
#   scripts/lint.sh                  tous les .md du dépôt (hors ressources/, build/, docs/)
#   scripts/lint.sh fichier.md ...   fichiers donnés (les non-.md sont ignorés)
#
# Sortie : une ligne par violation "fichier:ligne: [Rn] message". Code 1 si au
# moins une violation, 0 sinon.
#
# Pour ajouter une règle : un bloc `check_Rn` ci-dessous, appelé dans `lint_file`.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
violations=0

# R1 : pas de tiret long (U+2014) dans le texte.
check_R1() {
  local f="$1"
  grep -n -- '—' "$f" | while IFS= read -r line; do
    echo "$f:${line%%:*}: [R1] tiret long (U+2014) interdit, utiliser « : », une virgule ou une nouvelle phrase"
  done
}

lint_file() {
  local f="$1"
  [[ "$f" == *.md ]] || return 0
  [[ -f "$f" ]] || return 0
  local out
  out="$(check_R1 "$f")"
  if [[ -n "$out" ]]; then
    echo "$out"
    violations=$((violations + $(echo "$out" | wc -l | tr -d ' ')))
  fi
}

if [[ $# -eq 0 ]]; then
  while IFS= read -r f; do
    lint_file "$f"
  done < <(find "$ROOT" -name '*.md' \
    -not -path "$ROOT/ressources/*" \
    -not -path "$ROOT/build/*" \
    -not -path "$ROOT/docs/*" \
    -not -path "$ROOT/node_modules/*" | sort)
else
  for f in "$@"; do
    lint_file "$f"
  done
fi

if [[ $violations -gt 0 ]]; then
  echo "lint : $violations violation(s)" >&2
  exit 1
fi
exit 0
