"""Tests de scripts/avancement.py : python3 -m unittest scripts/tests/test_avancement.py"""
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    "avancement", pathlib.Path(__file__).resolve().parents[1] / "avancement.py")
assert spec is not None and spec.loader is not None
av = importlib.util.module_from_spec(spec)
spec.loader.exec_module(av)


def seq(i, code, minutes, statut, assignee="bauduinquentinn@gmail.com"):
    return {"identifier": i, "title": f"01 · {code} · Titre", "status": statut,
            "description": f"Durée apprenant : {minutes} min", "assignee": assignee,
            "parentId": None, "labels": ["chapitre"]}


def res(i, parent, statut, labels=()):
    return {"identifier": i, "title": "ressource", "status": statut,
            "assignee": "Kaan", "parentId": parent, "labels": list(labels)}


class TestAvancement(unittest.TestCase):
    def test_pourcentage_par_sequence(self):
        issues = [seq("A", "S1.1", 40, "Done"), seq("B", "S1.2", 60, "Todo")]
        r = av.analyser(issues)
        self.assertEqual((r["fait"], r["total"]), (40, 100))

    def test_annexe_hors_pourcentage_mais_listee(self):
        issues = [seq("A", "S1.1", 40, "Todo"), res("R", "A", "Todo", ["annexe"])]
        r = av.analyser(issues)
        self.assertEqual(r["fait"], 0)
        self.assertEqual(len(r["membres"]["Kaan"]["annexe_ouvert"]), 1)

    def test_sequence_done_avec_ressource_ouverte_est_signalee(self):
        issues = [seq("A", "S1.1", 40, "Done"), res("R", "A", "Todo")]
        self.assertTrue(av.analyser(issues)["alertes"])

    def test_depot_annexe_ouvert_sous_sequence_done_est_signale(self):
        issues = [seq("A", "S1.1", 40, "Done"), res("R", "A", "Todo", ["annexe"])]
        r = av.analyser(issues)
        self.assertEqual(r["fait"], 40)
        self.assertEqual(len(r["alertes"]), 1)

    def test_depot_annexe_ouvert_ne_declenche_pas_a_clore(self):
        issues = [seq("A", "S1.1", 40, "Todo"), res("R", "A", "Todo", ["annexe"])]
        self.assertFalse(av.analyser(issues)["alertes"])

    def test_sequence_a_clore(self):
        issues = [seq("A", "S1.1", 40, "Todo"), res("R", "A", "Done")]
        self.assertTrue(av.analyser(issues)["alertes"])

    def test_membres(self):
        self.assertEqual(av.membre("timo"), "Timothé")
        self.assertEqual(av.membre("erwing2002@gmail.com"), "Erwin")
        self.assertEqual(av.membre({"displayName": "kaantopkaya32"}), "Kaan")
        self.assertEqual(av.membre(None), "Non assigné")


if __name__ == "__main__":
    unittest.main()
