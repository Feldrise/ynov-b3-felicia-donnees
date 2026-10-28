#!/usr/bin/env python3
"""`make verify` : le contrôle de fin du dépôt (spec, Testing Decisions, sections A, B et C).

Étapes, dans l'ordre :
   0. lint du vocabulaire et de la charte (C)          6. mesure de l'effet de dénormalisation (A5)
   1. démarrage des cinq bases (A1)                     7. contrôle des schémas Mocodo (B)
   2. génération et chargement du jeu de données (A2)   8. régénération des PDF et contrôle des polices (A7)
   3. budget de démarrage < 5 minutes (A6)              9. construction et audit de l'export étudiant
   4. cohérence entre les bases (A3)                   10. destruction de l'environnement (A8)
   5. rejeu des requêtes recensées (A4)
Le projet Docker Compose porte un nom propre au dossier : plusieurs copies du dépôt peuvent se vérifier
en même temps sans se gêner. Dans l'export étudiant, les étapes 0, 7, 8 et 9 sont sautées.
Options : --garder (ne pas détruire les bases à la fin).
"""
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
EXPORT = (RACINE / ".export-etudiant").exists()
BUDGET_S = 300
PY = sys.executable

resultats = []


def etape(nom, cmd=None, fonction=None, formateur=False):
    print(f"\n== {nom}", flush=True)
    if formateur and EXPORT:
        print("  sautée dans l'export étudiant")
        resultats.append((nom, None, 0.0))
        return None
    debut = time.monotonic()
    try:
        if fonction is not None:
            ok = fonction()
        else:
            ok = subprocess.run(cmd, cwd=RACINE).returncode == 0
    except Exception as e:           # noqa: BLE001 - une étape qui plante est une étape en échec
        print(f"  KO   {type(e).__name__} : {e}")
        ok = False
    duree = time.monotonic() - debut
    resultats.append((nom, ok, duree))
    return ok


def preparer_outils():
    if (RACINE / ".venv" / "bin" / "mocodo").exists():
        return True
    print("  installation de Mocodo dans .venv")
    return (subprocess.run([PY, "-m", "venv", str(RACINE / ".venv")]).returncode == 0 and
            subprocess.run([str(RACINE / ".venv" / "bin" / "pip"), "install", "-q", "-r",
                            str(RACINE / "requirements.txt")]).returncode == 0)


def main():
    garder = "--garder" in sys.argv
    projet = "felicia-verif-" + hashlib.sha1(str(RACINE).encode()).hexdigest()[:8]
    os.environ["COMPOSE_PROJECT_NAME"] = projet
    compose = ["docker", "compose", "-f", str(RACINE / "compose.yaml")]
    print(f"Vérification du dépôt ({'export étudiant' if EXPORT else 'dossier du formateur'}), projet {projet}")

    etape("Lint du vocabulaire et de la charte (contrôle C)", [PY, "outils/lint_vocabulaire.py"], formateur=True)
    etape("Outils Python du formateur (Mocodo)", fonction=preparer_outils, formateur=True)
    etape("Tirage des images Docker (hors budget)", compose + ["pull", "--quiet"])
    budget = {}
    try:
        def demarrer():
            debut = time.monotonic()
            generation = subprocess.Popen([PY, "donnees/generer.py", "build/donnees"], cwd=RACINE,
                                          stdout=subprocess.DEVNULL)
            ok = subprocess.run(compose + ["up", "-d", "--wait", "--wait-timeout", str(BUDGET_S)], cwd=RACINE).returncode == 0
            ok = generation.wait() == 0 and ok
            budget["demarrage"] = time.monotonic() - debut
            print(f"  bases prêtes et données générées en {budget['demarrage']:.0f} s")
            return ok
        demarre = etape("Démarrage des cinq bases (A1)", fonction=demarrer)

        def charger():
            debut = time.monotonic()
            ok = subprocess.run(["bash", "outils/charger.sh"], cwd=RACINE).returncode == 0
            budget["chargement"] = time.monotonic() - debut
            return ok
        if demarre:
            charge = etape("Chargement du jeu de données Félicia (A2)", fonction=charger)

            def verifier_budget():
                total = budget.get("demarrage", 0) + budget.get("chargement", 0)
                print(f"  démarrage {budget.get('demarrage', 0):.0f} s + chargement {budget.get('chargement', 0):.0f} s"
                      f" = {total:.0f} s (budget {BUDGET_S} s)")
                return total < BUDGET_S
            etape("Budget de démarrage inférieur à 5 minutes (A6)", fonction=verifier_budget)
            if charge:
                etape("Cohérence entre les cinq bases (A3)", [PY, "outils/coherence.py"])
                etape("Rejeu des requêtes recensées (A4)", [PY, "outils/manifeste.py", "requetes"])
                etape("Effet de la dénormalisation (A5)", [PY, "outils/manifeste.py", "mesures"])
            etape("Schémas Mocodo : génération, inspection, chargement SQL (contrôle B)",
                  [PY, "outils/controle_mocodo.py"], formateur=True)
        else:
            etape("Schémas Mocodo sans base de données (contrôle B partiel)",
                  [PY, "outils/controle_mocodo.py", "--sans-sql"], formateur=True)
        etape("Régénération des PDF et contrôle des polices (A7)", [PY, "pdf/construire.py", "--tout"], formateur=True)
        etape("Export étudiant sans corrigé ni document formateur", [PY, "outils/exporter.py"], formateur=True)
    finally:
        if garder:
            print(f"\n== Bases conservées (projet {projet}) : COMPOSE_PROJECT_NAME={projet} make down pour les détruire")
        else:
            etape("Destruction de l'environnement (A8)", compose + ["down", "-v", "--remove-orphans", "--timeout", "5"])

    print("\n== Bilan")
    for nom, ok, duree in resultats:
        statut = "sautée" if ok is None else "ok" if ok else "ÉCHEC"
        print(f"  {statut:<7} {duree:6.1f} s  {nom}")
    echecs = [n for n, ok, _ in resultats if ok is False]
    print(f"\nmake verify : {'ÉCHEC (' + str(len(echecs)) + ' étape(s))' if echecs else 'tout est vert'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
