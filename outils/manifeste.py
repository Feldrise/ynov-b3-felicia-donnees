#!/usr/bin/env python3
"""Rejoue les requêtes recensées dans verification/requetes/**/*.toml (contrôle A, étapes 4 et 5).

Chaque ticket ajoute son propre fichier .toml ; les corrigés vont dans un sous-dossier formateur/,
exclu de l'export étudiant. Format :

  [[requete]]                      # rejouée dans l'ordre des fichiers (triés par chemin), puis du fichier
  id = "s3-mongo-legendaires"      # identifiant unique
  base = "mongo"                   # postgres | mongo | redis | cassandra | neo4j
  requete = "db.tresors.find({rarete: 'légendaire'})"   # ou fichier = "chemin/depuis/la/racine"
  lignes = 600                     # attendu : nombre de lignes,
  # valeur = "600"                 #   ou valeur de l'unique cellule,
  # contient = "Falaise des Soupirs"   ou texte présent dans la sortie (seul attendu possible avec fichier),
  # erreur = "ALLOW FILTERING"     #   ou échec attendu, avec ce texte dans le message (une limite démontrée)
  extrait_de = "demonstrations/s3/x.js"   # facultatif : la requête doit figurer dans ce fichier (espaces ignorés),
                                   # pour qu'un script de démonstration et son rejeu ne divergent pas

  [[mesure]]                       # PostgreSQL : la requête rapide doit battre la lente
  id = "s2-profil-heros"
  base = "postgres"
  lente = "SELECT ..."             # ou lente_fichier = "..."
  rapide = "SELECT ..."            # ou rapide_fichier = "..."
  facteur_min = 2.0                # temps médian (EXPLAIN ANALYZE) lente >= facteur_min x rapide
  repetitions = 5
  extrait_de = ["ateliers/s2/1-profil-jointures.sql", "ateliers/s2/2-profil-table.sql"]
                                   # facultatif : lente et rapide doivent figurer chacune dans l'un de ces fichiers

Une requête PostgreSQL ou MongoDB s'écrit comme une expression unique (MongoDB : curseur, tableau ou valeur).
Une requête Redis est une commande (« ZREVRANGE classement:saison:4 0 9 »).
"""
import json
import re
import statistics
import sys
import tomllib
from pathlib import Path

import bases

RACINE = bases.RACINE
DOSSIER = RACINE / "verification" / "requetes"
EXPORT = (RACINE / ".export-etudiant").exists()


def charger():
    requetes, mesures, erreurs = [], [], []
    ids = set()
    for f in sorted(DOSSIER.rglob("*.toml")):
        try:
            d = tomllib.loads(f.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            erreurs.append(f"{f.relative_to(RACINE)} : TOML invalide ({e})")
            continue
        for genre, liste in (("requete", requetes), ("mesure", mesures)):
            for e in d.get(genre, []):
                e["_fichier"] = f.relative_to(RACINE)
                if e.get("id") in ids or not e.get("id"):
                    erreurs.append(f"{e['_fichier']} : id absent ou en double ({e.get('id')})")
                ids.add(e.get("id"))
                if e.get("base") not in bases.BASES:
                    erreurs.append(f"{e['_fichier']} {e.get('id')} : base inconnue {e.get('base')!r}")
                liste.append(e)
    return requetes, mesures, erreurs


def texte(e, cle):
    """Texte de la requête (clé directe ou clé_fichier). None si le fichier manque dans l'export."""
    if cle in e:
        return e[cle]
    chemin = RACINE / e[f"{cle}_fichier"] if f"{cle}_fichier" in e else None
    if chemin is None:
        raise ValueError(f"ni {cle} ni {cle}_fichier")
    if not chemin.exists():
        if EXPORT:
            return None
        raise FileNotFoundError(f"fichier absent : {e[f'{cle}_fichier']}")
    return chemin.read_text(encoding="utf-8")


def sans_espaces(t):
    return re.sub(r"\s+", "", t)


def rejouer_requete(e):
    client = bases.CLIENTS[e["base"]]
    if "extrait_de" in e:
        source = RACINE / e["extrait_de"]
        if not source.exists():
            if EXPORT:
                return None, "sautée (fichier absent de l'export)"
            return False, f"fichier absent : {e['extrait_de']}"
        if "requete" not in e or sans_espaces(e["requete"]) not in sans_espaces(source.read_text(encoding="utf-8")):
            return False, f"requête absente de {e['extrait_de']}"
    if "fichier" in e:
        chemin = RACINE / e["fichier"]
        if not chemin.exists():
            if EXPORT:
                return None, "sautée (fichier absent de l'export)"
            return False, f"fichier absent : {e['fichier']}"
        res = client(fichier_texte=chemin.read_text(encoding="utf-8"))
    else:
        res = client(requete=e["requete"])
    if "erreur" in e:
        message = (res.erreur or "") + res.sortie
        if res.ok:
            return False, "réussie alors qu'un échec était attendu"
        if e["erreur"] not in message:
            return False, f"échec sans le texte attendu ({message.strip()[:300]})"
        return True, "échec attendu"
    if not res.ok:
        return False, f"erreur ({(res.erreur or res.sortie).strip()[:400]})"
    if "lignes" in e and len(res.lignes) != e["lignes"]:
        return False, f"{len(res.lignes)} lignes au lieu de {e['lignes']}"
    if "valeur" in e and res.valeur != str(e["valeur"]):
        return False, f"valeur {res.valeur!r} au lieu de {str(e['valeur'])!r}"
    if "contient" in e and e["contient"] not in res.sortie:
        return False, f"la sortie ne contient pas {e['contient']!r}"
    if not any(k in e for k in ("lignes", "valeur", "contient")) and "fichier" not in e:
        return False, "aucun résultat attendu déclaré (lignes, valeur ou contient)"
    detail = (f"{len(res.lignes)} lignes" if "lignes" in e else
              f"valeur {res.valeur}" if "valeur" in e else "sortie conforme" if "contient" in e else "exécuté")
    return True, detail


def temps_execution(requete, repetitions):
    temps = []
    for _ in range(repetitions):
        res = bases.postgres(f"EXPLAIN (ANALYZE, FORMAT JSON) {requete.strip().rstrip(';')}")
        if not res.ok:
            raise RuntimeError((res.erreur or res.sortie).strip()[:400])
        temps.append(json.loads("".join(res.lignes))[0]["Execution Time"])
    return statistics.median(temps)


def mesurer(e):
    if e["base"] != "postgres":
        return False, "seules les mesures PostgreSQL sont prises en charge"
    lente, rapide = texte(e, "lente"), texte(e, "rapide")
    if lente is None or rapide is None:
        return None, "sautée (fichier absent de l'export)"
    if "extrait_de" in e:
        sources = [RACINE / f for f in ([e["extrait_de"]] if isinstance(e["extrait_de"], str) else e["extrait_de"])]
        if not all(f.exists() for f in sources):
            return (None, "sautée (fichier absent de l'export)") if EXPORT else (False, "fichier extrait_de absent")
        contenu = [sans_espaces(f.read_text(encoding="utf-8")) for f in sources]
        for nom, requete in (("lente", lente), ("rapide", rapide)):
            if not any(sans_espaces(requete) in c for c in contenu):
                return False, f"requête {nom} absente de {', '.join(map(str, e['extrait_de'] if isinstance(e['extrait_de'], list) else [e['extrait_de']]))}"
    n = int(e.get("repetitions", 5))
    t_lente, t_rapide = temps_execution(lente, n), temps_execution(rapide, n)
    facteur = float(e.get("facteur_min", 2.0))
    detail = f"lente {t_lente:.2f} ms, rapide {t_rapide:.2f} ms (gain x{t_lente / max(t_rapide, 1e-6):.1f}, minimum x{facteur})"
    return t_lente >= facteur * t_rapide, detail


def main(etape="tout"):
    requetes, mesures, erreurs = charger()
    for err in erreurs:
        print(f"  KO   {err}")
    echecs = len(erreurs)
    if etape in ("tout", "requetes"):
        print(f"  {len(requetes)} requêtes recensées")
        for e in requetes:
            try:
                ok, detail = rejouer_requete(e)
            except Exception as ex:          # noqa: BLE001 - on rapporte toute erreur de rejeu
                ok, detail = False, str(ex)
            print(f"  {'--  ' if ok is None else 'ok  ' if ok else 'KO  '} {e['id']:<40} {e['base']:<10} {detail}")
            echecs += ok is False
    if etape in ("tout", "mesures"):
        if not mesures:
            print("  aucune mesure déclarée")
        for e in mesures:
            try:
                ok, detail = mesurer(e)
            except Exception as ex:          # noqa: BLE001
                ok, detail = False, str(ex)
            print(f"  {'--  ' if ok is None else 'ok  ' if ok else 'KO  '} {e['id']:<40} {detail}")
            echecs += ok is False
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "tout"))
