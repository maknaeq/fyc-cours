#!/usr/bin/env bash
# Exporte les fichiers Markdown du cours et des livrables en docx via pandoc.
#
# Usage :
#   scripts/build.sh                     tout (cours/ et livrables/)
#   scripts/build.sh cours/01-intro      un chapitre (fichiers concaténés)
#   scripts/build.sh livrables/x.md      un fichier
#
# La mise en page vient de charte/reference.docx.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF="$ROOT/charte/reference.docx"
OUT="$ROOT/build"
mkdir -p "$OUT"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc introuvable. Installer avec : brew install pandoc" >&2
  exit 1
fi

if [[ ! -f "$REF" ]]; then
  echo "charte/reference.docx manquant. Générer un défaut avec : scripts/init-reference.sh" >&2
  exit 1
fi

PANDOC_OPTS=(
  --from markdown+smart
  --to docx
  --reference-doc "$REF"
  --resource-path "$ROOT"
  --toc --toc-depth 2
  --number-sections
  --metadata lang=fr-FR
)

export_file() {
  local src="$1"
  local name
  name="$(basename "${src%.md}")"
  echo "→ $src"
  pandoc "${PANDOC_OPTS[@]}" "$src" -o "$OUT/$name.docx"
}

export_chapter() {
  local dir="$1"
  local name
  name="$(basename "$dir")"
  local files=()
  for f in README.md cours.md exercices.md qcm.md; do
    [[ -f "$dir/$f" ]] && files+=("$dir/$f")
  done
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "  (aucun fichier md dans $dir)"
    return
  fi
  echo "→ $dir (${#files[@]} fichiers)"
  pandoc "${PANDOC_OPTS[@]}" --resource-path "$dir:$ROOT" "${files[@]}" -o "$OUT/$name.docx"
}

if [[ $# -eq 0 ]]; then
  for d in "$ROOT"/cours/*/; do
    [[ -d "$d" ]] && export_chapter "${d%/}"
  done
  for f in "$ROOT"/livrables/*.md; do
    [[ -f "$f" ]] && export_file "$f"
  done
else
  for target in "$@"; do
    target="${target%/}"
    if [[ -d "$target" ]]; then
      export_chapter "$target"
    elif [[ -f "$target" ]]; then
      export_file "$target"
    else
      echo "Cible introuvable : $target" >&2
      exit 1
    fi
  done
fi

echo "Sorties dans $OUT/"
