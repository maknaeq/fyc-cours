#!/usr/bin/env bash
# Génère charte/reference.docx à partir du reference.docx par défaut de pandoc.
# Ouvrir ensuite ce fichier dans Word pour modifier les styles (Titre 1, Normal,
# Code source, etc.) : c'est ce fichier qui porte la charte graphique.
# Ne pas modifier le contenu du document, seulement les styles.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/charte/reference.docx"

if [[ -f "$OUT" ]]; then
  echo "$OUT existe déjà. Supprimer d'abord pour régénérer." >&2
  exit 1
fi

pandoc -o custom-reference.docx --print-default-data-file reference.docx
mv custom-reference.docx "$OUT"
echo "Créé : $OUT"
