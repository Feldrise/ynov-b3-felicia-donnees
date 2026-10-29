---
title: Les quatre paradigmes NoSQL
soustitre: Choisir le bon outil pour chaque besoin de Félicia
surtitre: Séance 3 · Vendredi 13 novembre, 8h00 à 12h00
public: Support étudiant
---

## Au programme

Clinique du Familier (15 min), tour d'horizon guidé (45 min), pause (10 min), groupes experts (1 h), redistribution (40 min), grille de choix et « Demande au Familier » (20 min), Boss et revue croisée (20 min), lancement de la Note 2 (30 min).

Rien à préparer avant ni après : tout se fait ici.

## Rouvrir son Codespace [3 min]{.duree}

Sur le temps de la Clinique, rouvre ton Codespace de la Séance 2 depuis **github.com/codespaces**, puis lance `make up` et laisse tourner (deux minutes environ). À « environnement prêt », `make etat` doit montrer les cinq bases.

::: {.encadre .attention}
Un Codespace s'arrête après 30 minutes d'inactivité : s'il s'est arrêté, rouvre-le et relance `make up` au début des groupes experts. Si ça échoue, mets-toi à deux sur un Codespace (fin du guide « Ouvrir son Codespace »).
:::

## Clinique du Familier [15 min]{.duree}

On décortique quelques prompts d'étudiants, anonymisés : ce qui marche, ce qui échoue, comment les améliorer. Ce qu'on en retient pour la Note 2 :

- **donne le contexte métier** : règles, chiffres, termes du Fil rouge ;
- **demande une justification et des hypothèses** (« explique chaque cardinalité ») ;
- **découpe** : une question par prompt, vérifiée avant la suivante ;
- **garde le dernier mot** : le Familier propose, tu décides, ton Journal du Familier dit pourquoi.

## Pourquoi sortir du relationnel ?

Le relationnel reste **le choix par défaut** : transactions, cohérence, questions imprévues. On n'en sort que si un besoin chiffré l'exige. Ton Codespace n'a qu'un échantillon ; voici Félicia en production, selon le studio :

| Besoin | Chiffres prévus en production | Ce qui coince en relationnel |
|-------------------------|------------------------------------------------|-------------------------------------------------|
| Les Trésors | 4,5 millions de Trésors, six natures aux attributs différents, une nouvelle nature à chaque Saison | une colonne par attribut possible, presque toutes vides, et une migration du schéma à chaque Saison |
| Classement et Vies | 45 000 Héros connectés le soir, 2 000 gains de Renommée par seconde, classement affiché en moins de 50 ms | trier un million de Héros à chaque affichage ; des écritures concurrentes sur les mêmes lignes |
| Télémétrie des Vies perdues | chaque Vie perdue arrive avec les 30 dernières secondes de position et d'actions du Héros : environ 2 milliards de lignes par Saison, écrites depuis trois régions (Europe, Canada, Afrique de l'Ouest), jamais modifiées | une seule machine écrit et stocke tout ; une panne de région bloque les écritures |
| Réseau des Clans | 9 000 Clans, 25 000 alliances ; « les alliés d'alliés », « le chemin diplomatique le plus court », à profondeur variable | une jointure de plus par niveau d'alliance, et une requête récursive dont le coût explose avec la profondeur |

## Le théorème CAP, en version Félicia

Félicia tourne en Europe et au Canada. Un soir, le câble entre les deux est coupé : c'est une **partition** (le P de CAP). Chaque région doit alors choisir entre la **cohérence (C)**, refuser tant qu'elle ne peut pas vérifier auprès de l'autre, et la **disponibilité (A)**, servir tout de suite et réconcilier plus tard, quitte à montrer deux versions un moment. Pas les deux à la fois, et ça se choisit **par besoin** :

| Demande pendant la coupure | Choix raisonnable | Pourquoi |
|------------------------------------|-------------------|--------------------------------------------------------|
| Acheter un Trésor avec ses Pelotes d'or | cohérence | dépenser deux fois les mêmes Pelotes d'or crée de la monnaie : on préfère refuser |
| Enregistrer une Vie perdue dans la télémétrie | disponibilité | perdre l'événement est pire que le ranger avec quelques secondes de retard |
| Afficher le classement de la Saison | disponibilité | un classement vieux de quelques secondes ne gêne personne |
| Retirer la dernière Vie d'un Héros | cohérence | un Héros ne doit jamais perdre une dixième Vie |

Sans coupure, le compromis reste, en plus petit : attendre les autres serveurs coûte de la **latence**. C'est la ligne « transactions » de la grille de choix.

## Tour d'horizon : quatre paradigmes, quatre besoins de Félicia

Je joue les démonstrations à l'écran ; rejoue-les en même temps depuis `demonstrations/s3/` (`make mongosh`, `make redis-cli`, `make cqlsh`, `make cypher-shell`).

### Document (MongoDB) : les Trésors [9 min]{.duree}

Chaque Trésor est un document JSON, avec ses propres champs : dégâts pour une arme, sorts pour un grimoire. Ce qui se lit ensemble se range ensemble. Forces : structure variable, pas de migration. Limites : pas de jointure ; une donnée recopiée (le nom du Clan) se met à jour partout. Script `1-mongo-tresors.js`.

### Clé-valeur (Redis) : classement temps réel et compteur de Vies [9 min]{.duree}

Retour de la **Renommée**, laissée de côté en Séance 1. Une clé, une valeur, en mémoire : le classement de la Saison (`classement:saison:4`), le compteur de Vies, une Convalescence qui expire seule. Forces : la milliseconde, l'atomicité, l'expiration. Limites : lecture par la clé seulement ; volume borné par la RAM. Script `2-redis-classement-vies.redis`.

### Colonne (Cassandra) : la télémétrie des Vies perdues [9 min]{.duree}

Une table par question. La **clé de partition** dit sur quel serveur vivent les lignes, les **colonnes de regroupement** dans quel ordre : une Vie perdue s'écrit dans `vies_par_ile` et dans `vies_par_heros`. Forces : écritures massives, sur plusieurs régions, sans point unique de panne. Limites : une question non prévue est refusée (« ALLOW FILTERING »), regroupement limité aux colonnes de la clé ; ni jointure ni transaction entre partitions. Script `3-cassandra-telemetrie.cql`.

### Graphe (Neo4j) : le réseau des Clans [9 min]{.duree}

Retour des **alliés d'alliés**, laissés de côté en Séance 1. Des nœuds et des relations nommées ; une requête dessine un motif : `(c:Clan)-[:ALLIE_A*2]-(autre:Clan)`. Forces : profondeur variable, coût proportionnel à ce qu'on parcourt. Limites : peu adapté aux agrégats massifs (« combien de Vies perdues par zone ? »). Scripts `4-neo4j-clans.cypher`, et la même question en SQL dans `4-postgres-alliances.sql`.

## Groupes experts et redistribution

Pendant une heure, votre groupe devient **expert d'un paradigme** : Tickets du Game Designer, puis fiche synthèse. Ensuite, en groupe mixte, chacun présente le sien en 8 minutes et tous complètent la fiche commune.

::: {.encadre .astuce}
Mon conseil : tu vas **enseigner** ton paradigme. Note ce qui t'a surpris ou bloqué, c'est ce que les autres doivent entendre.
:::

## La grille de choix, construite ensemble

On la remplit au tableau ; recopie quelques mots par case. Une case vide ? La grille de référence, remise ensuite pour le Boss et la Note 2, la complétera.

::: {.remplir .libelles .grille}
| Critère | Relationnel | Document | Clé-valeur | Colonne | Graphe |
|-----------------------------|-------------|------------|------------|------------|------------|
| 1 · Structure des données | | | | | |
| 2 · Volume | | | | | |
| 3 · Latence | | | | | |
| 4 · Besoin de transactions | | | | | |
| 5 · Relations | | | | | |
:::

**« Demande au Familier »** : je pose une question d'architecture au Familier ; relève les écarts entre sa recommandation et la grille.

[ ]{.a-remplir}

[ ]{.a-remplir}

[ ]{.a-remplir}
