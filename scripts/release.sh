#!/usr/bin/env bash
# Publie un jalon : exporte tous les docx, les archive dans livrables/archives/,
# crée un tag git et une release GitHub avec les fichiers attachés.
#
# Usage :
#   scripts/release.sh seance-2 "Séance 2 : scénarisation finale, biblio, 20 % des supports"
#
# Prérequis : sur main, dépôt propre, gh authentifié, pandoc installé.
# La release est l'endroit centralisé des rendus : coller son lien dans le
# jalon Linear et dans les issues concernées.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TAG="${1:-}"; TITLE="${2:-}"
if [[ -z "$TAG" || -z "$TITLE" ]]; then
  echo "Usage : scripts/release.sh <tag> \"<titre>\"   ex. scripts/release.sh seance-2 \"Séance 2 : ...\"" >&2
  exit 1
fi
cd "$ROOT"
if [[ "$(git branch --show-current)" != "main" ]]; then echo "Se placer sur main d'abord." >&2; exit 1; fi
if [[ -n "$(git status --porcelain)" ]]; then echo "Dépôt non propre : commiter ou remiser avant." >&2; exit 1; fi
if git rev-parse "$TAG" >/dev/null 2>&1; then echo "Le tag $TAG existe déjà." >&2; exit 1; fi

DATE="$(date +%Y-%m-%d)"
DEST="livrables/archives/$DATE-$TAG"
mkdir -p "$DEST"

echo "→ Export docx"
scripts/build.sh >/dev/null
cp build/*.docx "$DEST/"
echo "→ Archivé dans $DEST ($(ls "$DEST" | wc -l | tr -d ' ') fichiers)"

git add "$DEST"
git commit -q -m "Rendu $TAG : archive des docx exportés le $DATE"
git tag -a "$TAG" -m "$TITLE"
git push -q origin main "$TAG"

echo "→ Release GitHub"
gh release create "$TAG" "$DEST"/*.docx --title "$TITLE" --notes "Rendus exportés le $DATE depuis \`main\`. Archive : \`$DEST/\`."
gh release view "$TAG" --json url -q .url
