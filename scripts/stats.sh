#!/usr/bin/env bash
# Compte les signes du contenu écrit et affiche l'équivalent en pages
# (1 page = 4 000 signes, cible du FYC : ~30 pages).
# Lit aussi la durée apprenant déclarée dans le README.md de chaque chapitre
# (ligne "Durée apprenant : Xh" ou "X min").

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf "%-32s %10s %8s %10s\n" "Chapitre" "Signes" "Pages" "Durée"
printf "%-32s %10s %8s %10s\n" "--------" "------" "-----" "-----"

total_chars=0
total_min=0
for d in "$ROOT"/cours/*/; do
  [[ -d "$d" ]] || continue
  name="$(basename "$d")"
  chars=0
  for f in "$d"cours.md "$d"exercices.md "$d"qcm.md; do
    [[ -f "$f" ]] && chars=$((chars + $(wc -m < "$f")))
  done
  mins=0
  if [[ -f "$d/README.md" ]]; then
    line="$(grep -i 'durée apprenant' "$d/README.md" | head -1 || true)"
    h="$(echo "$line" | grep -oE '[0-9]+([.,][0-9]+)? ?h' | head -1 | tr -d 'h ' | tr ',' '.' || true)"
    m="$(echo "$line" | grep -oE '[0-9]+ ?min' | head -1 | tr -d 'min ' || true)"
    [[ -n "$h" ]] && mins=$(python3 -c "print(int(float('$h')*60))")
    [[ -n "$m" ]] && mins=$((mins + m))
  fi
  pages=$(python3 -c "print(f'{$chars/4000:.1f}')")
  printf "%-32s %10d %8s %7dmin\n" "$name" "$chars" "$pages" "$mins"
  total_chars=$((total_chars + chars))
  total_min=$((total_min + mins))
done

printf "%-32s %10s %8s %10s\n" "--------" "------" "-----" "-----"
pages=$(python3 -c "print(f'{$total_chars/4000:.1f}')")
hours=$(python3 -c "print(f'{$total_min/60:.1f}')")
printf "%-32s %10d %8s %8sh\n" "TOTAL (cible : 30 p, 10-15 h)" "$total_chars" "$pages" "$hours"
