#!/usr/bin/env python3
"""Génère le jeu de données de « Neuf Vies : Les Îles de Félicia ».

Une seule source, déterministe (graine fixe) : les cinq bases reçoivent les mêmes
Joueurs, Héros, Lignées, Clans, Trésors, Pelotes d'or et Vies, avec les mêmes identifiants.

Usage : python3 donnees/generer.py [dossier_de_sortie]   (par défaut build/donnees)

Sorties :
  csv/        une table PostgreSQL par fichier (servent aussi à Neo4j)
  mongo/      documents des collections heros, clans, tresors (JSON, un document par ligne)
  redis/      commandes au protocole RESP pour `redis-cli --pipe`
  cassandra/  tables dénormalisées par requête
  resume.json effectifs attendus, relus par la vérification de cohérence
"""
import csv
import json
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

GRAINE = 20261109          # date de la première Séance
NB_JOUEURS = 4000
NB_CLANS = 120
TAILLE_MAX_CLAN = 50
MAINTENANT = datetime(2026, 11, 8, 23, 0, tzinfo=timezone.utc)   # « aujourd'hui » dans le jeu
SAISON_COURANTE = 4
VIES_PAR_SAISON = 9

LIGNEES = [
    (1, "Sorcier", "Lance des sorts liés à un élément qu'il maîtrise."),
    (2, "Rôdeur d'ombre", "Se faufile sans être vu ; sa furtivité se mesure de 1 à 100."),
    (3, "Gardien", "Protège son Clan ; la solidité de son rempart se mesure de 1 à 100."),
    (4, "Alchimiste", "Prépare potions et élixirs à partir des recettes qu'il connaît."),
]
ELEMENTS = ["feu", "givre", "foudre", "lune", "lierre"]

# (id, nom, niveau requis, zones, poids de danger)
ILES = [
    (1, "Brume", 25, ["Falaise des Soupirs", "Marais Sans Fond", "Pont des Lierres", "Phare Éteint"], 9),
    (2, "Velours", 1, ["Prairie des Coussins", "Port aux Nuages", "Moulin à Pelotes"], 2),
    (3, "Croc-de-Pierre", 10, ["Carrière des Échos", "Col du Grand Croc", "Gouffre Ronronnant"], 5),
    (4, "Lune-Rousse", 35, ["Observatoire Brisé", "Jardins Suspendus", "Escalier des Mille Marches"], 6),
    (5, "Ronces", 15, ["Labyrinthe d'Épines", "Clairière aux Corbeaux", "Source Amère"], 4),
    (6, "Cendres", 45, ["Volcan Assoupi", "Forge des Anciens", "Plaine Calcinée"], 7),
    (7, "Grand-Ronron", 5, ["Marché Flottant", "Arène des Novices", "Bibliothèque Volante"], 3),
    (8, "Nuit-Sans-Fin", 55, ["Cathédrale d'Ombre", "Abîme des Murmures", "Trône Vacant"], 8),
]
# Sur l'île de Brume, la Falaise des Soupirs est de loin la zone la plus meurtrière.
POIDS_ZONES_BRUME = [6, 2, 2, 1]

SAISONS = [
    (1, "Saison du Premier Ronron", date(2025, 12, 1), date(2026, 2, 28)),
    (2, "Saison des Lanternes", date(2026, 3, 1), date(2026, 5, 31)),
    (3, "Saison des Brumes Hautes", date(2026, 6, 1), date(2026, 8, 31)),
    (4, "Saison de la Lune Rousse", date(2026, 9, 1), date(2026, 11, 30)),
]

CAUSES = ["chute dans le vide", "sortilège", "gardien d'île", "duel", "piège", "brume toxique"]
POIDS_CAUSES = [30, 20, 18, 14, 10, 8]

NATURES = ["arme", "armure", "grimoire", "potion", "relique", "parure"]
RARETES = ["commun", "rare", "épique", "légendaire"]
POIDS_RARETES = [56, 28, 14, 2]

MOTIFS = ["quête", "revente de Trésor", "récompense de saison", "achat en boutique", "cotisation de Clan", "achat avec argent réel"]

PAYS = ["FR"] * 12 + ["BE"] * 3 + ["CH"] * 2 + ["CA"] * 3 + ["MA", "SN", "LU", "CI", "TN"]

PRENOMS = """Minou Félix Caramel Moka Pistache Réglisse Pacha Tigrou Brindille Grisou Plume Cannelle Ombre
Givre Noisette Biscotte Chaussette Mistigri Pompon Zéphyr Saphir Opale Croquette Filou Gribouille Moustique
Patapouf Ronron Câline Fripouille Praline Muscade Nougat Vanille Paprika Sésame Chicorée Grignote Frimousse
Pirouette Bergamote Capucine Églantine Hermine Indigo Jasmin Kiwi Lavande Mirabelle Nuage Orage Perle Quenotte
Rubis Safran Tonnerre Ursule Violette Wasabi Yuzu Zinzolin Albâtre Basilic Cobalt Dragée Ébène Fenouil Galet
Hibiscus Iris Jade Lichen Mandarine Nacre Origan Poivre Quartz Romarin Silex Tilleul Ambre Bambou
Anis Bruine Cassis Datura Écume Figue Gingembre Houblon Ivoire Jonquille Kumquat Lilas Mélisse Nénuphar
Orchidée Pervenche Rhubarbe Sauge Tamaris Vétiver Azur Bourrasque Calcite Dune Étincelle Fougère Grêle
Hirondelle Ibis Javelot Kaolin Luciole Myrtille Nectar Obsidienne Pollen Réséda Sorbet Topaze Verveine""".split()
EPITHETES = """des-Brumes Patte-de-Velours le-Hardi Griffe-d'Argent Œil-de-Lune Queue-Fourchue Moustaches-Folles
Cœur-de-Givre la-Discrète le-Rêveur Pelage-d'Or Croc-Brisé l'Insomniaque la-Vagabonde Sans-Peur Pas-de-Loup
Oreille-Fendue le-Sage la-Rusée Poil-Hérissé Griffe-Noire le-Pensif l'Intrépide Patte-Agile Ronron-Tonnerre
Chasse-Étoiles Saute-Nuages la-Flamboyante le-Taciturne Moustache-Fière Bout-de-Queue Œil-de-Braise l'Errant
la-Silencieuse Croque-Lune Fil-d'Ombre le-Doux Vif-Argent Danse-Brume la-Téméraire Coussinet-Agile
Patte-Blanche Gris-Perle l'Ancien Feu-Follet Sourcil-Froncé la-Curieuse Rôde-Toits le-Gourmand Plume-de-Nuit
Mâche-Lierre Grand-Sommeil Mille-Vies la-Lointaine Pique-Étoile Œil-Vairon Frisson-d'Hiver le-Magnifique
Pelote-Folle Chat-Perché Saute-Ruisseau le-Distrait la-Prudente Brise-Roche Lune-Pleine Herbe-Folle""".split()
MOTS_PSEUDO = """nyx miaou neko tigre lynx puma ronron pixel ombre givre lune brume caramel kawa zephyr rubis onyx
jade tonnerre foudre plume griffe patte moustache velours sirocco blizzard quartz orage cobalt""".split()

CLAN_TETES = ["Les Griffes", "Les Moustaches", "L'Ordre", "La Confrérie", "Les Veilleurs", "Les Pattes",
              "Le Cercle", "Les Enfants", "La Meute", "Les Gardiens", "Les Chasseurs", "Les Ronronneurs"]
CLAN_QUEUES = ["de l'Aube", "du Crépuscule", "de la Lune Rousse", "des Brumes", "du Lierre", "d'Argent",
               "des Cendres", "du Velours", "de la Nuit", "des Ronces", "du Grand Croc", "des Étoiles Filantes"]
DEVISES = ["Neuf Vies, un seul Clan.", "Toujours retomber sur ses pattes.", "La nuit nous appartient.",
           "Patte de velours, griffe d'acier.", "Qui ronronne veille.", "Plus haut que les nuages.",
           "Jamais deux fois la même chute.", "La brume ne nous fait pas peur."]

NOMS_TRESORS = {
    "arme": ["Griffe", "Dague", "Bâton", "Arc", "Fouet de lierre", "Sabre courbe"],
    "armure": ["Cuirasse", "Cape", "Bottes", "Heaume", "Collier de mailles"],
    "grimoire": ["Grimoire", "Codex", "Recueil", "Carnet de sorts"],
    "potion": ["Élixir", "Philtre", "Fiole", "Tisane"],
    "relique": ["Clochette", "Pelote ancienne", "Miroir", "Sablier", "Plume de phénix"],
    "parure": ["Amulette", "Grelot", "Bague", "Ruban", "Médaillon"],
}
QUALIFICATIFS = ["de Brume", "du Croissant", "d'Ébène", "ronronnant", "des Marées", "de l'Aube",
                 "du Vagabond", "des Cendres", "de Velours", "d'Opale", "du Lierre", "des Neuf Vies"]
LEGENDAIRES = ["Griffe d'Aube", "Cape de Minuit", "Codex des Neuf Vies", "Élixir du Premier Ronron",
               "Clochette de Lune Rousse", "Pelote Originelle", "Miroir des Brumes", "Sablier Sans Fin",
               "Couronne du Trône Vacant", "Arc des Étoiles Filantes", "Plume du Phénix Gris",
               "Amulette de Félicia", "Heaume du Gardien Éternel", "Fouet de la Ronce Mère",
               "Médaillon des Cendres", "Bottes du Saute-Nuages", "Grelot du Silence", "Dague de Velours Noir",
               "Bâton de la Marée Haute", "Ruban de l'Aurore"]
SURNOMS_LEGENDAIRES = ["", " primordial", " oublié", " maudit", " béni", " du Nord", " du Sud", " jumeau",
                       " ancestral", " retrouvé", " brisé", " renaissant", " céleste", " des abysses",
                       " d'automne", " d'hiver", " de printemps", " d'été", " sacré", " perdu",
                       " des origines", " des marées", " éternel", " solaire", " lunaire", " voilé",
                       " écarlate", " d'argent", " d'or", " de jade"]


def lisible(epithete):
    """« des-Brumes » devient « des Brumes » ; « Patte-de-Velours » reste tel quel."""
    if epithete[0].islower():
        return epithete.replace("-", " ", 1)
    return epithete


def iso(d):
    return d.isoformat()


def horodatage(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S+0000")


def jour_aleatoire(rng, debut, fin):
    return debut + timedelta(days=rng.randrange((fin - debut).days + 1))


def instant_aleatoire(rng, debut, fin):
    secondes = int((fin - debut).total_seconds())
    return debut + timedelta(seconds=rng.randrange(max(secondes, 1)))


def debut_jour(d):
    return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)


def attributs_tresor(rng, nature, rarete):
    puissance = {"commun": 1, "rare": 2, "épique": 3, "légendaire": 5}[rarete]
    if nature == "arme":
        a = {"degats": rng.randint(5, 20) * puissance, "allonge": rng.choice(["courte", "moyenne", "longue"])}
        if rng.random() < 0.4:
            a["element"] = rng.choice(ELEMENTS)
    elif nature == "armure":
        a = {"defense": rng.randint(4, 15) * puissance, "poids_kg": round(rng.uniform(0.3, 6.0), 1)}
    elif nature == "grimoire":
        a = {"ecole": rng.choice(ELEMENTS),
             "sorts": rng.sample(["Bond lunaire", "Voile de brume", "Griffe de foudre", "Sommeil profond",
                                  "Ronron guérisseur", "Mur de lierre", "Pluie de givre", "Flamme féline"],
                                 k=min(1 + puissance, 6))}
    elif nature == "potion":
        a = {"effet": rng.choice(["soin", "vitesse", "invisibilité", "vision nocturne", "résistance au vide"]),
             "duree_s": rng.choice([30, 60, 120, 300]) * puissance, "doses": rng.randint(1, 3)}
    elif nature == "relique":
        a = {"pouvoir": rng.choice(["rappel au repaire", "chute amortie", "détection des pièges", "écho du passé"]),
             "charges": rng.randint(1, 3) * puissance, "maudite": rng.random() < 0.15}
    else:
        stat = rng.choice(["agilité", "sagesse", "endurance", "chance"])
        a = {"emplacement": rng.choice(["cou", "oreille", "queue", "patte"]), "bonus": {stat: rng.randint(1, 5) * puissance}}
    return a


def generer(sortie: Path):
    rng = random.Random(GRAINE)
    saison_par_id = {s[0]: s for s in SAISONS}
    zones = []
    zone_par_ile = {}
    for id_ile, _, _, noms_zones, _ in ILES:
        for nom in noms_zones:
            zones.append((len(zones) + 1, id_ile, nom))
            zone_par_ile.setdefault(id_ile, []).append(len(zones))
    niveau_ile = {i[0]: i[2] for i in ILES}
    nom_ile = {i[0]: i[1] for i in ILES}
    zone_par_id = {z[0]: z for z in zones}

    # Joueurs
    joueurs = []
    pseudos = set()
    courriels = set()
    for id_joueur in range(1, NB_JOUEURS + 1):
        while True:
            pseudo = f"{rng.choice(MOTS_PSEUDO)}{rng.choice(['', '_', '.'])}{rng.choice(MOTS_PSEUDO)}{rng.randint(1, 999)}"
            courriel = f"{pseudo.replace('.', '_')}@felicia.test"
            if pseudo not in pseudos and courriel not in courriels:
                pseudos.add(pseudo)
                courriels.add(courriel)
                break
        inscription = jour_aleatoire(rng, date(2025, 9, 1), date(2026, 10, 31))
        joueurs.append({"id_joueur": id_joueur, "pseudo": pseudo, "courriel": courriel,
                        "pays": rng.choice(PAYS), "date_inscription": inscription})

    # Héros : un Joueur en possède un ou plusieurs
    noms_heros = [f"{p} {lisible(e)}" for p in PRENOMS for e in EPITHETES]
    rng.shuffle(noms_heros)
    heros = []
    for j in joueurs:
        nb = rng.choices([1, 2, 3, 4], weights=[52, 28, 13, 7])[0]
        for _ in range(nb):
            id_heros = len(heros) + 1
            id_lignee = rng.choice([1, 1, 2, 2, 3, 3, 4])
            creation = jour_aleatoire(rng, j["date_inscription"], date(2026, 11, 1))
            anciennete = (date(2026, 11, 8) - creation).days
            niveau = max(1, min(60, int(rng.gauss(anciennete / 7, 6)) + 1))
            h = {"id_heros": id_heros, "nom": noms_heros.pop(), "id_joueur": j["id_joueur"], "id_lignee": id_lignee,
                 "niveau": niveau, "renommee": 0, "date_creation": creation, "id_clan": None, "date_adhesion": None,
                 "id_mentor": None, "date_debut_mentorat": None, "element": None, "furtivite": None, "rempart": None, "recettes_connues": None}
            if id_lignee == 1:
                h["element"] = rng.choice(ELEMENTS)
            elif id_lignee == 2:
                h["furtivite"] = rng.randint(1, 100)
            elif id_lignee == 3:
                h["rempart"] = rng.randint(1, 100)
            else:
                h["recettes_connues"] = rng.randint(1, 40)
            heros.append(h)
    heros_par_id = {h["id_heros"]: h for h in heros}

    # Mentorat : un apprenti a au plus un mentor, plus expérimenté, d'un autre Joueur
    mentors_possibles = [h for h in heros if h["niveau"] >= 30]
    for h in heros:
        if h["niveau"] < 20 and rng.random() < 0.3:
            for _ in range(10):
                m = rng.choice(mentors_possibles)
                if m["id_joueur"] != h["id_joueur"]:
                    h["id_mentor"] = m["id_heros"]
                    break
    # Date de début du mentorat (Ticket n°2 de la Séance 1) : tirée par un générateur à part,
    # pour ne pas décaler la suite du jeu de données (effectifs cités dans les supports).
    rng_mentorat = random.Random(GRAINE + 1)
    for h in heros:
        if h["id_mentor"]:
            debut = max(h["date_creation"], heros_par_id[h["id_mentor"]]["date_creation"])
            h["date_debut_mentorat"] = jour_aleatoire(rng_mentorat, debut, max(debut, date(2026, 11, 7)))

    # Clans : chaque Héros en rejoint au plus un ; le chef est un membre
    noms_clans = [f"{t} {q}" for t in CLAN_TETES for q in CLAN_QUEUES]
    rng.shuffle(noms_clans)
    clans = []
    for id_clan in range(1, NB_CLANS + 1):
        clans.append({"id_clan": id_clan, "nom": noms_clans.pop(), "devise": rng.choice(DEVISES),
                      "date_fondation": jour_aleatoire(rng, date(2025, 10, 15), date(2026, 9, 30)),
                      "id_ile_repaire": rng.choice([i[0] for i in ILES]), "id_heros_chef": None})
    membres = {c["id_clan"]: [] for c in clans}
    taille_cible = {c["id_clan"]: rng.randint(8, TAILLE_MAX_CLAN) for c in clans}
    for h in heros:
        if rng.random() < 0.72:
            candidats = [c for c in clans if len(membres[c["id_clan"]]) < taille_cible[c["id_clan"]]]
            if not candidats:
                continue
            c = rng.choice(candidats)
            h["id_clan"] = c["id_clan"]
            debut = max(c["date_fondation"], h["date_creation"])
            h["date_adhesion"] = jour_aleatoire(rng, debut, max(debut, date(2026, 11, 7)))
            membres[c["id_clan"]].append(h["id_heros"])
    for c in clans:
        ids = membres[c["id_clan"]]
        chef = max(ids, key=lambda i: (heros_par_id[i]["niveau"], -i))
        c["id_heros_chef"] = chef
        # le chef a rejoint son Clan dès sa fondation (ou dès sa création s'il est plus jeune)
        heros_par_id[chef]["date_adhesion"] = max(c["date_fondation"], heros_par_id[chef]["date_creation"])

    # Alliances entre Clans (graphe non orienté, stocké avec id_clan_1 < id_clan_2)
    alliances = {}
    for c in clans:
        for _ in range(rng.choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]):
            autre = rng.randint(1, NB_CLANS)
            if autre == c["id_clan"]:
                continue
            a, b = sorted((c["id_clan"], autre))
            if (a, b) not in alliances:
                debut = max(clans[a - 1]["date_fondation"], clans[b - 1]["date_fondation"])
                alliances[(a, b)] = jour_aleatoire(rng, debut, max(debut, date(2026, 11, 1)))
    alliances = [{"id_clan_1": a, "id_clan_2": b, "date_alliance": d} for (a, b), d in sorted(alliances.items())]

    # Vies perdues : au plus 9 par Héros et par saison, numérotées de 1 à 9
    vies = []
    poids_iles = [i[4] for i in ILES]
    for h in heros:
        for id_saison, _, debut_s, fin_s in SAISONS:
            debut = max(debut_jour(debut_s), debut_jour(h["date_creation"]))
            fin = min(debut_jour(fin_s) + timedelta(days=1), MAINTENANT)
            if debut >= fin:
                continue
            part = (fin - debut).total_seconds() / ((fin_s - debut_s).days * 86400)
            if rng.random() < 0.08 * part:
                nb = VIES_PAR_SAISON          # Héros endormi jusqu'à la saison suivante
            else:
                nb = min(8, int(rng.choices(range(9), weights=[3, 4, 6, 8, 10, 13, 15, 14, 12])[0] * min(1.0, part + 0.25)))
            instants = sorted(instant_aleatoire(rng, debut, fin) for _ in range(nb))
            for numero, instant in enumerate(instants, start=1):
                accessibles = [i for i in ILES if i[2] <= h["niveau"]]
                ile = rng.choices(accessibles, weights=[i[4] for i in accessibles])[0]
                if ile[0] == 1:
                    id_zone = rng.choices(zone_par_ile[1], weights=POIDS_ZONES_BRUME)[0]
                else:
                    id_zone = rng.choice(zone_par_ile[ile[0]])
                cause = rng.choices(CAUSES, weights=POIDS_CAUSES)[0]
                if ile[0] == 1 and zone_par_id[id_zone][2] == "Falaise des Soupirs" and rng.random() < 0.5:
                    cause = "chute dans le vide"
                vainqueur = None
                if cause == "duel":
                    while (vainqueur is None or vainqueur == h["id_heros"]
                           or heros_par_id[vainqueur]["date_creation"] > instant.date()):
                        vainqueur = rng.randint(1, len(heros))
                vies.append({"id_vie": len(vies) + 1, "id_heros": h["id_heros"], "id_saison": id_saison,
                             "numero": numero, "date_heure": instant, "id_zone": id_zone, "cause": cause,
                             "id_heros_vainqueur": vainqueur})
    del poids_iles

    # Trésors : obtenus par un Héros sur une île (association ternaire) ; les légendaires changent de mains
    tresors, obtentions, possessions = [], [], []
    noms_legendaires = [f"{n}{s}" for s in SURNOMS_LEGENDAIRES for n in LEGENDAIRES]
    for h in heros:
        nb = min(15, int(rng.expovariate(1 / 5)))
        for _ in range(nb):
            id_tresor = len(tresors) + 1
            nature = rng.choice(NATURES)
            rarete = rng.choices(RARETES, weights=POIDS_RARETES)[0]
            if rarete == "légendaire" and noms_legendaires:
                nom = noms_legendaires.pop(0)
            else:
                if rarete == "légendaire":
                    rarete = "épique"
                nom = f"{rng.choice(NOMS_TRESORS[nature])} {rng.choice(QUALIFICATIFS)}"
            accessibles = [i[0] for i in ILES if i[2] <= h["niveau"]]
            id_ile = rng.choice(accessibles)
            obtenu = instant_aleatoire(rng, debut_jour(h["date_creation"]), MAINTENANT)
            proprietaire = h["id_heros"]
            if rarete == "légendaire":
                debut = obtenu
                detenteur = h["id_heros"]
                for _ in range(rng.randint(0, 3)):
                    fin = instant_aleatoire(rng, debut, MAINTENANT)
                    possessions.append({"id_tresor": id_tresor, "id_heros": detenteur, "date_debut": debut, "date_fin": fin})
                    candidats = [x for x in heros if x["date_creation"] <= fin.date() and x["id_heros"] != detenteur]
                    detenteur = rng.choice(candidats)["id_heros"]
                    debut = fin
                possessions.append({"id_tresor": id_tresor, "id_heros": detenteur, "date_debut": debut, "date_fin": None})
                proprietaire = detenteur
            tresors.append({"id_tresor": id_tresor, "nom": nom, "nature": nature, "rarete": rarete,
                            "attributs": attributs_tresor(rng, nature, rarete), "id_heros_proprietaire": proprietaire})
            obtentions.append({"id_tresor": id_tresor, "id_heros": h["id_heros"], "id_ile": id_ile, "date_obtention": obtenu})

    # Pelotes d'or : la bourse d'un Héros ne descend jamais sous zéro
    transactions = []
    for h in heros:
        debut = debut_jour(h["date_creation"])
        nb = int(rng.uniform(20, 130))
        instants = sorted(instant_aleatoire(rng, debut, MAINTENANT) for _ in range(nb))
        solde = 0
        for instant in instants:
            motif = rng.choices(MOTIFS, weights=[40, 18, 4, 25, 8, 5])[0]
            if motif in ("quête", "revente de Trésor", "récompense de saison", "achat avec argent réel"):
                montant = rng.randint(5, 120) * (5 if motif == "achat avec argent réel" else 1)
            else:
                montant = -rng.randint(5, 150)
                if solde + montant < 0:
                    motif, montant = "quête", rng.randint(5, 60)
            solde += montant
            transactions.append({"id_transaction": len(transactions) + 1, "id_heros": h["id_heros"],
                                 "date_heure": instant, "montant": montant, "motif": motif})
        h["pelotes"] = solde

    # Renommée de la saison courante (sert au classement temps réel)
    vies_courantes = {}
    for v in vies:
        if v["id_saison"] == SAISON_COURANTE:
            vies_courantes[v["id_heros"]] = vies_courantes.get(v["id_heros"], 0) + 1
    for h in heros:
        if h["date_creation"] <= date(2026, 11, 8):
            h["renommee"] = max(0, int(h["niveau"] * rng.uniform(20, 60) - 40 * vies_courantes.get(h["id_heros"], 0)))
        h["vies_restantes"] = VIES_PAR_SAISON - vies_courantes.get(h["id_heros"], 0)

    ecrire(sortie, joueurs, heros, clans, alliances, zones, vies, tresors, obtentions, possessions, transactions,
           nom_ile, zone_par_id, membres)


def ecrire_csv(chemin, colonnes, lignes):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(colonnes)
        for ligne in lignes:
            w.writerow(["" if v is None else v for v in ligne])


def ecrire(sortie, joueurs, heros, clans, alliances, zones, vies, tresors, obtentions, possessions, transactions,
           nom_ile, zone_par_id, membres):
    c = sortie / "csv"
    ecrire_csv(c / "lignee.csv", ["id_lignee", "nom", "description"], LIGNEES)
    ecrire_csv(c / "ile.csv", ["id_ile", "nom", "niveau_requis"], [(i[0], i[1], i[2]) for i in ILES])
    ecrire_csv(c / "zone.csv", ["id_zone", "id_ile", "nom"], zones)
    ecrire_csv(c / "saison.csv", ["id_saison", "nom", "date_debut", "date_fin"],
               [(s[0], s[1], iso(s[2]), iso(s[3])) for s in SAISONS])
    ecrire_csv(c / "joueur.csv", ["id_joueur", "pseudo", "courriel", "pays", "date_inscription"],
               [(j["id_joueur"], j["pseudo"], j["courriel"], j["pays"], iso(j["date_inscription"])) for j in joueurs])
    ecrire_csv(c / "clan.csv", ["id_clan", "nom", "devise", "date_fondation", "id_ile_repaire", "id_heros_chef"],
               [(x["id_clan"], x["nom"], x["devise"], iso(x["date_fondation"]), x["id_ile_repaire"], x["id_heros_chef"])
                for x in clans])
    colonnes_heros = ["id_heros", "nom", "id_joueur", "id_lignee", "niveau", "renommee", "date_creation", "id_clan",
                      "date_adhesion", "id_mentor", "date_debut_mentorat", "element", "furtivite", "rempart", "recettes_connues"]
    ecrire_csv(c / "heros.csv", colonnes_heros,
               [[iso(h[k]) if isinstance(h[k], date) else h[k] for k in colonnes_heros] for h in heros])
    ecrire_csv(c / "alliance.csv", ["id_clan_1", "id_clan_2", "date_alliance"],
               [(a["id_clan_1"], a["id_clan_2"], iso(a["date_alliance"])) for a in alliances])
    ecrire_csv(c / "tresor.csv", ["id_tresor", "nom", "nature", "rarete", "attributs", "id_heros_proprietaire"],
               [(t["id_tresor"], t["nom"], t["nature"], t["rarete"], json.dumps(t["attributs"], ensure_ascii=False),
                 t["id_heros_proprietaire"]) for t in tresors])
    ecrire_csv(c / "obtention.csv", ["id_tresor", "id_heros", "id_ile", "date_obtention"],
               [(o["id_tresor"], o["id_heros"], o["id_ile"], horodatage(o["date_obtention"])) for o in obtentions])
    ecrire_csv(c / "possession_tresor.csv", ["id_tresor", "id_heros", "date_debut", "date_fin"],
               [(p["id_tresor"], p["id_heros"], horodatage(p["date_debut"]),
                 horodatage(p["date_fin"]) if p["date_fin"] else None) for p in possessions])
    ecrire_csv(c / "vie_perdue.csv", ["id_vie", "id_heros", "id_saison", "numero", "date_heure", "id_zone", "cause",
                                      "id_heros_vainqueur"],
               [(v["id_vie"], v["id_heros"], v["id_saison"], v["numero"], horodatage(v["date_heure"]), v["id_zone"],
                 v["cause"], v["id_heros_vainqueur"]) for v in vies])
    ecrire_csv(c / "transaction_pelotes.csv", ["id_transaction", "id_heros", "date_heure", "montant", "motif"],
               [(t["id_transaction"], t["id_heros"], horodatage(t["date_heure"]), t["montant"], t["motif"])
                for t in transactions])

    heros_par_id = {h["id_heros"]: h for h in heros}
    joueur_par_id = {j["id_joueur"]: j for j in joueurs}
    clan_par_id = {x["id_clan"]: x for x in clans}
    lignee_nom = {l[0]: l[1] for l in LIGNEES}
    obtention_par_tresor = {o["id_tresor"]: o for o in obtentions}
    historique = {}
    for p in possessions:
        historique.setdefault(p["id_tresor"], []).append(p)
    allies = {}
    for a in alliances:
        allies.setdefault(a["id_clan_1"], []).append(a["id_clan_2"])
        allies.setdefault(a["id_clan_2"], []).append(a["id_clan_1"])

    # MongoDB : un document par ligne (mongoimport), identifiant commun dans _id
    m = sortie / "mongo"
    m.mkdir(parents=True, exist_ok=True)
    with (m / "heros.json").open("w", encoding="utf-8") as f:
        for h in heros:
            doc = {"_id": h["id_heros"], "nom": h["nom"],
                   "joueur": {"id_joueur": h["id_joueur"], "pseudo": joueur_par_id[h["id_joueur"]]["pseudo"]},
                   "lignee": {"id_lignee": h["id_lignee"], "nom": lignee_nom[h["id_lignee"]]},
                   "niveau": h["niveau"], "renommee": h["renommee"], "vies_restantes": h["vies_restantes"],
                   "pelotes": h["pelotes"],
                   "clan": ({"id_clan": h["id_clan"], "nom": clan_par_id[h["id_clan"]]["nom"]} if h["id_clan"] else None),
                   "id_mentor": h["id_mentor"],
                   "date_debut_mentorat": iso(h["date_debut_mentorat"]) if h["date_debut_mentorat"] else None}
            for k in ("element", "furtivite", "rempart", "recettes_connues"):
                if h[k] is not None:
                    doc[k] = h[k]
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    with (m / "clans.json").open("w", encoding="utf-8") as f:
        for x in clans:
            f.write(json.dumps({"_id": x["id_clan"], "nom": x["nom"], "devise": x["devise"],
                                "date_fondation": iso(x["date_fondation"]),
                                "repaire": {"id_ile": x["id_ile_repaire"], "nom": nom_ile[x["id_ile_repaire"]]},
                                "id_heros_chef": x["id_heros_chef"], "allies": sorted(allies.get(x["id_clan"], [])),
                                "nb_membres": len(membres[x["id_clan"]])}, ensure_ascii=False) + "\n")
    with (m / "tresors.json").open("w", encoding="utf-8") as f:
        for t in tresors:
            o = obtention_par_tresor[t["id_tresor"]]
            doc = {"_id": t["id_tresor"], "nom": t["nom"], "nature": t["nature"], "rarete": t["rarete"],
                   "attributs": t["attributs"],
                   "proprietaire": {"id_heros": t["id_heros_proprietaire"],
                                    "nom": heros_par_id[t["id_heros_proprietaire"]]["nom"]},
                   "obtention": {"id_heros": o["id_heros"], "ile": nom_ile[o["id_ile"]],
                                 "date": {"$date": o["date_obtention"].strftime("%Y-%m-%dT%H:%M:%SZ")}}}
            if t["id_tresor"] in historique:
                doc["historique"] = [{"id_heros": p["id_heros"],
                                      "debut": {"$date": p["date_debut"].strftime("%Y-%m-%dT%H:%M:%SZ")},
                                      "fin": ({"$date": p["date_fin"].strftime("%Y-%m-%dT%H:%M:%SZ")}
                                              if p["date_fin"] else None)} for p in historique[t["id_tresor"]]]
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    # Redis : protocole RESP pour `redis-cli --pipe`
    r = sortie / "redis"
    r.mkdir(parents=True, exist_ok=True)

    def resp(*args):
        morceaux = [f"*{len(args)}\r\n".encode()]
        for a in args:
            b = str(a).encode("utf-8")
            morceaux.append(b"$" + str(len(b)).encode() + b"\r\n" + b + b"\r\n")
        return b"".join(morceaux)

    with (r / "charger.resp").open("wb") as f:
        f.write(resp("FLUSHDB"))
        for h in heros:
            f.write(resp("HSET", f"heros:{h['id_heros']}", "nom", h["nom"], "id_joueur", h["id_joueur"],
                         "lignee", lignee_nom[h["id_lignee"]], "niveau", h["niveau"], "id_clan", h["id_clan"] or "",
                         "vies_restantes", h["vies_restantes"], "renommee", h["renommee"], "pelotes", h["pelotes"]))
            f.write(resp("ZADD", f"classement:saison:{SAISON_COURANTE}", h["renommee"], h["id_heros"]))
        for x in clans:
            f.write(resp("HSET", f"clan:{x['id_clan']}", "nom", x["nom"], "devise", x["devise"],
                         "id_heros_chef", x["id_heros_chef"], "id_ile_repaire", x["id_ile_repaire"]))
            f.write(resp("SADD", f"clan:{x['id_clan']}:membres", *membres[x["id_clan"]]))
        for t in tresors:
            f.write(resp("HSET", f"tresor:{t['id_tresor']}", "nom", t["nom"], "nature", t["nature"],
                         "rarete", t["rarete"], "id_heros", t["id_heros_proprietaire"]))
            f.write(resp("SADD", f"heros:{t['id_heros_proprietaire']}:tresors", t["id_tresor"]))

    # Cassandra : une table par requête
    k = sortie / "cassandra"
    ecrire_csv(k / "heros.csv", ["id_heros", "nom", "id_joueur", "lignee", "niveau", "id_clan"],
               [(h["id_heros"], h["nom"], h["id_joueur"], lignee_nom[h["id_lignee"]], h["niveau"], h["id_clan"])
                for h in heros])
    ecrire_csv(k / "clans.csv", ["id_clan", "nom", "id_ile_repaire", "nb_membres"],
               [(x["id_clan"], x["nom"], x["id_ile_repaire"], len(membres[x["id_clan"]])) for x in clans])
    ecrire_csv(k / "tresors_par_heros.csv", ["id_heros", "id_tresor", "nom", "nature", "rarete"],
               [(t["id_heros_proprietaire"], t["id_tresor"], t["nom"], t["nature"], t["rarete"]) for t in tresors])
    ecrire_csv(k / "vies_par_heros.csv", ["id_heros", "id_saison", "numero", "date_heure", "ile", "zone", "cause",
                                          "id_heros_vainqueur"],
               [(v["id_heros"], v["id_saison"], v["numero"], horodatage(v["date_heure"]),
                 nom_ile[zone_par_id[v["id_zone"]][1]], zone_par_id[v["id_zone"]][2], v["cause"],
                 v["id_heros_vainqueur"]) for v in vies])
    ecrire_csv(k / "vies_par_ile.csv", ["id_ile", "id_saison", "zone", "date_heure", "id_heros", "numero", "cause",
                                        "id_clan"],
               [(zone_par_id[v["id_zone"]][1], v["id_saison"], zone_par_id[v["id_zone"]][2],
                 horodatage(v["date_heure"]), v["id_heros"], v["numero"], v["cause"],
                 heros_par_id[v["id_heros"]]["id_clan"]) for v in vies])

    # Neo4j : victoires en duel agrégées (qui a pris une Vie à qui)
    duels = {}
    for v in vies:
        if v["id_heros_vainqueur"]:
            cle = (v["id_heros_vainqueur"], v["id_heros"])
            duels[cle] = duels.get(cle, 0) + 1
    ecrire_csv(sortie / "neo4j" / "duels.csv", ["id_vainqueur", "id_vaincu", "nb"],
               [(a, b, n) for (a, b), n in sorted(duels.items())])

    resume = {
        "graine": GRAINE, "saison_courante": SAISON_COURANTE,
        "joueurs": len(joueurs), "heros": len(heros), "lignees": len(LIGNEES), "clans": len(clans),
        "alliances": len(alliances), "iles": len(ILES), "zones": len(zones), "saisons": len(SAISONS),
        "tresors": len(tresors), "tresors_legendaires": sum(t["rarete"] == "légendaire" for t in tresors),
        "possessions": len(possessions), "vies_perdues": len(vies),
        "vies_perdues_saison_courante": sum(v["id_saison"] == SAISON_COURANTE for v in vies),
        "transactions_pelotes": len(transactions), "heros_en_clan": sum(1 for h in heros if h["id_clan"]),
        "duels": len(duels),
    }
    (sortie / "resume.json").write_text(json.dumps(resume, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(resume, ensure_ascii=False))


if __name__ == "__main__":
    generer(Path(sys.argv[1] if len(sys.argv) > 1 else "build/donnees"))
