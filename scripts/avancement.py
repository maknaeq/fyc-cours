#!/usr/bin/env python3
"""Calcule l'avancement du cours par séquence à partir d'un export Linear.

Règles (cadrage du 25/11/2026, FYC-96) :
- une séquence est une issue dont le titre commence par `NN · Sx.y ·` (ou
  `00 · 00.y ·`) et dont la description contient `Durée apprenant : N min` ;
- le pourcentage = durée des séquences au statut Done / durée de toutes les
  séquences (900 min pour la trame V2) ;
- les issues au label `annexe` (dépôts de TP, Teams, avancement, soutenance,
  outillage) ne comptent pas dans le pourcentage : elles sont listées à part,
  membre par membre ;
- une séquence Done dont une ressource (annexe ou non) n'est pas Done est
  signalée : un dépôt de TP rattaché à sa séquence doit être livré avant
  qu'elle soit terminée.

Entrée : un fichier JSON, liste d'issues avec au minimum `identifier`, `title`,
`description`, `status` (ou `state.name`), `assignee` (texte ou
`displayName`), `parentId` (ou `parent.identifier`) et `labels` (liste de
noms ou `{"nodes": [{"name": ...}]}`). On l'obtient avec l'outil `list_issues`
de Linear (champs title, description, status, parentId, assignee, labels).

Usage :
    scripts/avancement.py export.json            # tableau Markdown sur stdout
    scripts/avancement.py export.json --json     # mêmes chiffres en JSON
"""
import json
import re
import sys
from collections import defaultdict

SEQ_TITLE = re.compile(r"^(\d\d)\s*·\s*((?:S\d|00)\.\d)\s*·\s*(.+)$")
DUREE = re.compile(r"Durée apprenant\s*:\s*(\d+)\s*min")
MEMBRES = ("Quentin", "Kaan", "Timothé", "Erwin")


def membre(assignee):
    """Ramène un assigné (email, displayName, nom) à l'un des 4 membres."""
    if isinstance(assignee, dict):
        assignee = assignee.get("displayName") or assignee.get("name") or ""
    a = (assignee or "").lower()
    for cle, nom in (("quentin", "Quentin"), ("kaan", "Kaan"),
                     ("timo", "Timothé"), ("erwin", "Erwin")):
        if cle in a:
            return nom
    return "Non assigné"


def statut(issue):
    s = issue.get("status") or issue.get("state") or ""
    return s.get("name", "") if isinstance(s, dict) else s


def parent(issue):
    p = issue.get("parentId") or issue.get("parent")
    return p.get("identifier") if isinstance(p, dict) else p


def labels(issue):
    ls = issue.get("labels") or []
    if isinstance(ls, dict):
        ls = ls.get("nodes", [])
    return {(x.get("name") if isinstance(x, dict) else x) for x in ls}


def ident(issue):
    return issue.get("identifier") or issue.get("id")


def analyser(issues):
    par_id = {ident(i): i for i in issues}
    sequences = {}
    for i in issues:
        m = SEQ_TITLE.match(i.get("title", ""))
        d = DUREE.search(i.get("description") or "")
        if m and d:
            sequences[ident(i)] = {
                "id": ident(i), "chapitre": m.group(1), "code": m.group(2),
                "titre": m.group(3), "duree": int(d.group(1)),
                "statut": statut(i), "membre": membre(i.get("assignee")),
            }
    enfants = defaultdict(list)
    for i in issues:
        p = parent(i)
        if p in sequences:
            enfants[p].append(i)

    alertes = []
    for sid, s in sequences.items():
        contenu = [c for c in enfants[sid] if "annexe" not in labels(c)
                   and statut(c) != "Canceled"]
        ouvertes = [ident(c) for c in contenu if statut(c) != "Done"]
        annexes_ouvertes = [ident(c) for c in enfants[sid] if "annexe" in labels(c)
                            and statut(c) not in ("Done", "Canceled")]
        if s["statut"] == "Done" and annexes_ouvertes:
            alertes.append(f"{sid} ({s['code']}) est Done mais ces dépôts annexe ne sont pas livrés : "
                           + ", ".join(annexes_ouvertes))
        if s["statut"] == "Done" and ouvertes:
            alertes.append(f"{sid} ({s['code']}) est Done mais ces ressources ne le sont pas : "
                           + ", ".join(ouvertes))
        if s["statut"] != "Done" and contenu and not ouvertes:
            alertes.append(f"{sid} ({s['code']}) a toutes ses ressources Done : à clore ?")

    total = sum(s["duree"] for s in sequences.values())
    fait = sum(s["duree"] for s in sequences.values() if s["statut"] == "Done")

    chapitres = defaultdict(lambda: [0, 0])
    par_membre = {m: {"seq_total": 0, "seq_fait": 0, "annexe_fait": 0,
                      "annexe_ouvert": [], "autres_ouvert": 0} for m in MEMBRES}
    par_membre["Non assigné"] = dict(par_membre["Quentin"], annexe_ouvert=[])
    for s in sequences.values():
        chapitres[s["chapitre"]][1] += s["duree"]
        par_membre[s["membre"]]["seq_total"] += s["duree"]
        if s["statut"] == "Done":
            chapitres[s["chapitre"]][0] += s["duree"]
            par_membre[s["membre"]]["seq_fait"] += s["duree"]

    for i in issues:
        if "annexe" not in labels(i) or statut(i) == "Canceled":
            continue
        m = par_membre[membre(i.get("assignee"))]
        if statut(i) == "Done":
            m["annexe_fait"] += 1
        else:
            m["annexe_ouvert"].append(f"{ident(i)} {i.get('title', '')}")
    return {"sequences": sequences, "total": total, "fait": fait,
            "chapitres": dict(chapitres), "membres": par_membre,
            "alertes": alertes}


def h(minutes):
    return f"{minutes // 60} h {minutes % 60:02d}"


def markdown(r):
    pct = 100 * r["fait"] / r["total"] if r["total"] else 0
    out = [f"**Avancement du cours : {pct:.0f} %** ({h(r['fait'])} sur {h(r['total'])} "
           f"de durée apprenant, séquences terminées).", ""]
    out += ["| Chapitre | Terminé | Total |", "|---|---:|---:|"]
    for c in sorted(r["chapitres"]):
        f, t = r["chapitres"][c]
        out.append(f"| {c} | {h(f)} | {h(t)} |")
    out += ["", "| Membre | Séquences terminées | Séquences portées | Tâches annexe terminées | Tâches annexe ouvertes |",
            "|---|---:|---:|---:|---:|"]
    for nom in MEMBRES:
        m = r["membres"][nom]
        out.append(f"| {nom} | {h(m['seq_fait'])} | {h(m['seq_total'])} | "
                   f"{m['annexe_fait']} | {len(m['annexe_ouvert'])} |")
    out += ["", "Tâches annexe ouvertes (hors pourcentage, comptées pour l'avancement individuel) :", ""]
    for nom in MEMBRES:
        ouvertes = r["membres"][nom]["annexe_ouvert"]
        if ouvertes:
            out.append(f"- **{nom}**")
            out += [f"  - {t}" for t in ouvertes]
    if r["alertes"]:
        out += ["", "À vérifier :", ""] + [f"- {a}" for a in r["alertes"]]
    return "\n".join(out)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(argv) > 1 else 2
    with open(argv[1], encoding="utf-8") as f:
        issues = json.load(f)
    if isinstance(issues, dict):
        issues = issues.get("issues", [])
    r = analyser(issues)
    if not r["sequences"]:
        print("Aucune séquence trouvée : titre `NN · Sx.y · …` et description "
              "`Durée apprenant : N min` attendus (voir l'en-tête du script).",
              file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2) if "--json" in argv
          else markdown(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
