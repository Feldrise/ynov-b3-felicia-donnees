#!/usr/bin/env python3
"""Vérifie la cohérence du jeu de données entre les cinq bases (contrôle A, étape 3).

Mêmes Héros, Clans et Trésors avec les mêmes identifiants partout ; mêmes liens
(Héros d'un Clan, propriétaire d'un Trésor, mentor et date de début du mentorat) ; même nombre de Vies perdues.
PostgreSQL fait référence : chaque autre base est comparée à lui.
"""
import json
import re
import sys

import bases


class Echec(Exception):
    pass


def lire(res, quoi):
    if not res.ok:
        raise Echec(f"{quoi} : la requête a échoué ({(res.erreur or res.sortie).strip()[:300]})")
    return res.lignes


def entiers(lignes):
    return {int(x.strip().strip('"')) for x in lignes if x.strip()}


def paires(lignes, sep):
    out = set()
    for l in lignes:
        a, b = [x.strip().strip('"') for x in l.split(sep)]
        if a not in ("", "null", "None") and b not in ("", "null", "None"):
            out.add((int(a), int(b)))
    return out


def mongo_json(expr, quoi):
    res = bases.mongo(f"JSON.stringify({expr})")
    lignes = lire(res, quoi)
    return json.loads(lignes[0])


def redis_cles(motif, regex):
    code, out, err = bases.exec_("redis", "redis-cli", "--scan", "--pattern", motif, "--count", "5000")
    if code != 0:
        raise Echec(f"Redis {motif} : {err.strip()}")
    return {int(m.group(1)) for k in out.split() if (m := re.fullmatch(regex, k))}


def comparer(nom, reference, autres, constats):
    for base, valeurs in autres.items():
        if valeurs == reference:
            print(f"  ok   {nom:<34} {base:<10} {len(valeurs)} identiques à PostgreSQL")
        else:
            manque, surplus = reference - valeurs, valeurs - reference
            constats.append(f"{nom} ({base}) : {len(manque)} absents, {len(surplus)} en trop "
                            f"(ex. {sorted(manque)[:3]} / {sorted(surplus)[:3]})")
            print(f"  KO   {nom:<34} {base:<10} {len(manque)} absents, {len(surplus)} en trop")


def verifier():
    constats = []
    pg = lambda q: lire(bases.postgres(q), f"PostgreSQL « {q} »")
    cq = lambda q: lire(bases.cassandra(q), f"Cassandra « {q} »")
    ne = lambda q: lire(bases.neo4j(q), f"Neo4j « {q} »")

    # Identifiants
    ref_heros = entiers(pg("SELECT id_heros FROM heros"))
    ref_clans = entiers(pg("SELECT id_clan FROM clan"))
    ref_tresors = entiers(pg("SELECT id_tresor FROM tresor"))
    ref_joueurs = entiers(pg("SELECT id_joueur FROM joueur"))
    comparer("Héros", ref_heros, {
        "mongo": set(mongo_json("db.heros.distinct('_id')", "MongoDB heros")),
        "redis": redis_cles("heros:*", r"heros:(\d+)"),
        "cassandra": entiers(cq("SELECT id_heros FROM heros")),
        "neo4j": entiers(ne("MATCH (h:Heros) RETURN h.id_heros")),
    }, constats)
    comparer("Clans", ref_clans, {
        "mongo": set(mongo_json("db.clans.distinct('_id')", "MongoDB clans")),
        "redis": redis_cles("clan:*", r"clan:(\d+)"),
        "cassandra": entiers(cq("SELECT id_clan FROM clans")),
        "neo4j": entiers(ne("MATCH (c:Clan) RETURN c.id_clan")),
    }, constats)
    comparer("Trésors", ref_tresors, {
        "mongo": set(mongo_json("db.tresors.distinct('_id')", "MongoDB tresors")),
        "redis": redis_cles("tresor:*", r"tresor:(\d+)"),
        "cassandra": entiers(cq("SELECT id_tresor FROM tresors_par_heros")),
        "neo4j": entiers(ne("MATCH (t:Tresor) RETURN t.id_tresor")),
    }, constats)
    comparer("Joueurs", ref_joueurs, {
        "mongo": set(mongo_json("db.heros.distinct('joueur.id_joueur')", "MongoDB joueurs")),
        "neo4j": entiers(ne("MATCH (j:Joueur) RETURN j.id_joueur")),
    }, constats)

    # Liens
    ref_membres = paires(pg("SELECT id_heros, id_clan FROM heros WHERE id_clan IS NOT NULL"), "|")
    code, out, err = bases.exec_("redis", "sh", "-c",
                                 "for k in $(redis-cli --scan --pattern 'clan:*:membres'); do "
                                 "echo \"#$k\"; redis-cli SMEMBERS \"$k\"; done")
    if code != 0:
        raise Echec(f"Redis membres : {err.strip()}")
    membres_redis, id_clan = set(), None
    for ligne in out.split():
        if ligne.startswith("#clan:"):
            id_clan = int(ligne.split(":")[1])
        else:
            membres_redis.add((int(ligne), id_clan))
    comparer("Héros membres d'un Clan", ref_membres, {
        "mongo": {(d["_id"], d["clan"]["id_clan"]) for d in
                  mongo_json("db.heros.find({clan: {$ne: null}}, {clan: 1}).toArray()", "MongoDB membres")},
        "redis": membres_redis,
        "cassandra": paires(cq("SELECT id_heros, id_clan FROM heros"), "|"),
        "neo4j": paires(ne("MATCH (h:Heros)-[:MEMBRE_DE]->(c:Clan) RETURN h.id_heros + '|' + c.id_clan"), "|"),
    }, constats)
    ref_proprietaires = paires(pg("SELECT id_tresor, id_heros_proprietaire FROM tresor"), "|")
    comparer("Propriétaire de chaque Trésor", ref_proprietaires, {
        "mongo": {(d["_id"], d["proprietaire"]["id_heros"]) for d in
                  mongo_json("db.tresors.find({}, {'proprietaire.id_heros': 1}).toArray()", "MongoDB propriétaires")},
        "cassandra": {(t, h) for h, t in paires(cq("SELECT id_heros, id_tresor FROM tresors_par_heros"), "|")},
        "neo4j": paires(ne("MATCH (h:Heros)-[:POSSEDE]->(t:Tresor) RETURN t.id_tresor + '|' + h.id_heros"), "|"),
    }, constats)

    # Mentorat : apprenti, mentor et date de début (Ticket n°2 de la Séance 1)
    ref_mentorat = set(pg("SELECT id_heros || '|' || id_mentor || '|' || date_debut_mentorat FROM heros "
                          "WHERE id_mentor IS NOT NULL"))
    comparer("Mentorat et date de début", ref_mentorat, {
        "mongo": {f"{d['_id']}|{d['id_mentor']}|{d['date_debut_mentorat']}" for d in
                  mongo_json("db.heros.find({id_mentor: {$ne: null}}, {id_mentor: 1, date_debut_mentorat: 1}).toArray()",
                             "MongoDB mentorat")},
        "neo4j": {l.strip().strip('"') for l in
                  ne("MATCH (m:Heros)-[r:MENTOR_DE]->(a:Heros) "
                     "RETURN a.id_heros + '|' + m.id_heros + '|' + toString(r.depuis)")},
    }, constats)

    # Vies perdues (règle des 9 Vies par saison)
    saison = int(pg("SELECT max(id_saison) FROM saison")[0])
    total = int(pg("SELECT count(*) FROM vie_perdue")[0])
    courante = int(pg(f"SELECT count(*) FROM vie_perdue WHERE id_saison = {saison}")[0])
    depassements = int(pg("SELECT count(*) FROM (SELECT 1 FROM vie_perdue GROUP BY id_heros, id_saison "
                          "HAVING count(*) > 9) x")[0])
    valeurs = {
        "Vies perdues (Cassandra, par Héros)": (total, int(cq("SELECT count(*) FROM vies_par_heros")[0])),
        "Vies perdues (Cassandra, par île)": (total, int(cq("SELECT count(*) FROM vies_par_ile")[0])),
        "Vies perdues cette saison (MongoDB)": (courante, mongo_json(
            "db.heros.aggregate([{$group: {_id: null, n: {$sum: {$subtract: [9, '$vies_restantes']}}}}]).toArray()[0].n",
            "MongoDB vies")),
        "Héros au-delà de 9 Vies (PostgreSQL)": (0, depassements),
    }
    code, out, err = bases.exec_("redis", "sh", "-c",
                                 "redis-cli --scan --pattern 'heros:*' | grep -E '^heros:[0-9]+$' | "
                                 "while read k; do echo \"HGET $k vies_restantes\"; done | redis-cli")
    if code != 0:
        raise Echec(f"Redis vies : {err.strip()}")
    restantes = [int(x) for x in out.split()]
    vies_redis = 9 * len(restantes) - sum(restantes)
    valeurs["Vies perdues cette saison (Redis)"] = (courante, vies_redis)
    for nom, (attendu, obtenu) in valeurs.items():
        if attendu == obtenu:
            print(f"  ok   {nom:<45} {obtenu}")
        else:
            constats.append(f"{nom} : attendu {attendu}, obtenu {obtenu}")
            print(f"  KO   {nom:<45} attendu {attendu}, obtenu {obtenu}")
    return constats


def main():
    try:
        constats = verifier()
    except Echec as e:
        print(f"  KO   {e}")
        return 1
    if constats:
        print("\n".join(f"  - {c}" for c in constats))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
