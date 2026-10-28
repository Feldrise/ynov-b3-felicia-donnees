---
title: Les quatre paradigmes NoSQL
soustitre: Choisir le bon outil pour chaque besoin de Félicia
surtitre: Séance 3 · Vendredi 13 novembre, 8h00 à 12h00
public: Support étudiant
---

## La Séance en un coup d'œil

::: bloc
| Heure | Bloc | Ce que vous faites |
|--------------|------------------------------------------|------------------------------------------------------------|
| 8h00 | Clinique du Familier [15 min]{.duree} | vous rouvrez votre Codespace, puis vous diagnostiquez des prompts réels et les améliorez |
| 8h15 | Tour d'horizon guidé [45 min]{.duree} | pourquoi sortir du relationnel, puis quatre démonstrations sur Félicia |
| 9h00 | Pause [10 min]{.duree} | |
| 9h10 | Groupes experts [1 h]{.duree} | votre groupe traite les Tickets du Game Designer d'un seul paradigme et rédige sa fiche synthèse |
| 10h10 | Redistribution [40 min]{.duree} | en groupe mixte, vous enseignez votre paradigme aux autres et apprenez les leurs |
| 10h50 | Grille de choix et « Demande au Familier » [20 min]{.duree} | la classe construit la grille de décision, puis la confronte au Familier |
| 11h10 | Boss et revue croisée [20 min]{.duree} | en trinôme, un paradigme justifié pour cinq besoins ; le trinôme voisin critique |
| 11h30 | Lancement de la Note 2 [30 min]{.duree} | votre Sujet de Note 2, tiré en Séance 2, relu avec votre trinôme |
:::

Rien n'est à préparer avant ni après la Séance : tout se fait ici.

## Rouvrir son Codespace [3 min]{.duree}

À 8h00, au début de la Clinique (ces 3 minutes font partie de ses 15 minutes) :

1. Ouvrez **github.com/codespaces** et cliquez sur le Codespace du module créé en Séance 2. Il redémarre en une minute environ.
2. Dans le terminal, tapez `make up`, puis laissez tourner : les cinq bases démarrent et Félicia se recharge (deux minutes environ). Vous pouvez suivre la Clinique pendant ce temps.
3. La commande se termine par « environnement prêt ». `make etat` affiche alors les cinq bases.

::: {.encadre .attention}
Un Codespace inactif s'arrête seul au bout de 30 minutes. S'il s'est arrêté pendant la pause, rouvrez-le et relancez `make up` dès le début des groupes experts. En cas d'échec, la procédure de secours est à la fin du guide « Ouvrir son Codespace » : on travaille à deux sur un même Codespace.
:::

## Clinique du Familier [15 min]{.duree}

On projette trois ou quatre prompts écrits par des étudiants (anonymisés) pendant les Séances 1 et 2 ou la Note 1. Pour chacun : ce qui fonctionne, ce qui échoue, et comment l'améliorer. Ce que l'on retient, et qui vous servira dès la Note 2 :

- **Donner le contexte métier** : les règles, les chiffres, les termes du Fil rouge, pas seulement « mon jeu ».
- **Demander une justification et des hypothèses**, pas seulement un résultat : « explique chaque cardinalité », « liste ce que tu as supposé ».
- **Découper** : une question par prompt, puis on vérifie avant de passer à la suivante.
- **Garder le dernier mot** : le Familier propose, vous décidez, et le Journal du Familier dit pourquoi.

## Pourquoi sortir du relationnel ?

Depuis la Séance 1, tout Félicia tient dans PostgreSQL, et c'est très bien : le relationnel reste **le choix par défaut**. Il garantit les transactions, interdit les incohérences et répond à des questions qu'on n'avait pas prévues. On n'en sort que lorsqu'un besoin chiffré l'exige.

Le jeu de données de votre Codespace est un échantillon. Voici les chiffres que le studio Griffe & Grimoire prévoit pour Félicia en production : ce sont eux qui font hésiter.

| Besoin | Chiffres prévus en production | Ce qui coince en relationnel |
|-------------------------|------------------------------------------------|-------------------------------------------------|
| Les Trésors | 4,5 millions de Trésors, six natures aux attributs différents, une nouvelle nature à chaque Saison | une colonne par attribut possible, presque toutes vides, et une migration du schéma à chaque Saison |
| Classement et Vies | 45 000 Héros connectés le soir, 2 000 gains de Renommée par seconde, classement affiché en moins de 50 ms | trier un million de Héros à chaque affichage ; des écritures concurrentes sur les mêmes lignes |
| Télémétrie des Vies perdues | chaque Vie perdue arrive avec les 30 dernières secondes de position et d'actions du Héros : environ 2 milliards de lignes par Saison, écrites depuis trois régions (Europe, Canada, Afrique de l'Ouest), jamais modifiées | une seule machine écrit et stocke tout ; une panne de région bloque les écritures |
| Réseau des Clans | 9 000 Clans, 25 000 alliances ; « les alliés d'alliés », « le chemin diplomatique le plus court », à profondeur variable | une jointure de plus par niveau d'alliance, et une requête récursive dont le coût explose avec la profondeur |

## Le théorème CAP, en version Félicia

Félicia tourne sur plusieurs serveurs, en Europe et au Canada. Un soir, le câble entre les deux régions est coupé : c'est une **partition** du réseau (le P de CAP). Chaque région continue de recevoir des demandes. Pour chacune, il faut choisir :

- **Cohérence (C)** : refuser la demande tant qu'on ne peut pas vérifier auprès de l'autre région. Personne ne lit jamais une donnée périmée, mais une partie des Joueurs reçoit une erreur.
- **Disponibilité (A, pour *availability*)** : accepter la demande tout de suite et réconcilier les deux régions plus tard. Tout le monde est servi, mais deux Joueurs peuvent voir, un moment, deux versions différentes.

Le théorème dit qu'en cas de partition, on ne peut pas avoir les deux. Ce n'est pas un choix de base de données une fois pour toutes, c'est un choix **par besoin** :

| Demande pendant la coupure | Choix raisonnable | Pourquoi |
|------------------------------------|-------------------|--------------------------------------------------------|
| Acheter un Trésor avec ses Pelotes d'or | cohérence | dépenser deux fois les mêmes Pelotes d'or crée de la monnaie : on préfère refuser |
| Enregistrer une Vie perdue dans la télémétrie | disponibilité | perdre l'événement est pire que le ranger avec quelques secondes de retard |
| Afficher le classement de la Saison | disponibilité | un classement vieux de quelques secondes ne gêne personne |
| Retirer la dernière Vie d'un Héros | cohérence | un Héros ne doit jamais perdre une dixième Vie |

Hors partition, le même compromis existe en plus petit : attendre la confirmation des autres serveurs (cohérence) coûte de la **latence**. C'est la question que pose la ligne « transactions » de la grille de choix.

## Tour d'horizon : quatre paradigmes, quatre besoins de Félicia

Le formateur rejoue ces démonstrations sur son écran. Les scripts sont dans votre Codespace, dans le dossier `demonstrations/s3/` : vous pouvez les rejouer en même temps, étape par étape, dans le terminal de la base (`make mongosh`, `make redis-cli`, `make cqlsh`, `make cypher-shell`).

### Document (MongoDB) : les Trésors [9 min]{.duree}

- **Le modèle** : chaque Trésor est un document JSON ; deux documents d'une même collection n'ont pas forcément les mêmes champs. Ce qui se lit ensemble se range ensemble : attributs, propriétaire, historique.
- **Sur Félicia** : une arme a des dégâts et une allonge, un grimoire une liste de sorts ; la Griffe d'Aube garde la liste de ses propriétaires successifs. Le studio ajoute un attribut sans migration.
- **Forces** : structure variable, lecture d'un agrégat en une seule fois, évolution sans migration.
- **Limites** : pas de jointure naturelle ; une donnée recopiée (le nom du Clan dans chaque Héros) doit être mise à jour partout par l'application.
- **Script** : `demonstrations/s3/1-mongo-tresors.js`.

### Clé-valeur (Redis) : classement temps réel et compteur de Vies [9 min]{.duree}

C'est ici que revient la **Renommée**, mise de côté pendant l'atelier de la Séance 1.

- **Le modèle** : une clé, une valeur, en mémoire. La valeur peut être un texte, un compteur, un hash, un ensemble, un ensemble trié.
- **Sur Félicia** : la fiche d'un Héros (`heros:3426`), le classement de la Saison trié par la Renommée (`classement:saison:4`), le compteur de Vies décrémenté de façon atomique, une convalescence qui expire seule.
- **Forces** : latence de l'ordre de la milliseconde, opérations atomiques, expiration automatique.
- **Limites** : on ne lit que par la clé, aucune requête sur le contenu ; les données vivent en mémoire, leur volume est borné par la RAM.
- **Script** : `demonstrations/s3/2-redis-classement-vies.redis`.

### Colonne (Cassandra) : la télémétrie des Vies perdues [9 min]{.duree}

- **Le modèle** : des tables dessinées pour une question précise. La **clé de partition** dit sur quel serveur vivent les lignes, les **colonnes de regroupement** dans quel ordre elles y sont rangées. Une même donnée est écrite dans autant de tables que de questions.
- **Sur Félicia** : `vies_par_ile` répond à « où les Héros perdent-ils leurs Vies sur cette Île cette Saison ? », `vies_par_heros` au journal d'un Héros. Une Vie perdue s'écrit dans les deux.
- **Forces** : écritures massives et réparties sur de nombreux serveurs et plusieurs régions, sans point unique de panne ; lecture rapide d'une partition dans l'ordre.
- **Limites** : une question non prévue est refusée (« ALLOW FILTERING ») ; regroupements limités aux colonnes de la clé ; pas de jointure ni de transaction entre partitions.
- **Script** : `demonstrations/s3/3-cassandra-telemetrie.cql`.

### Graphe (Neo4j) : le réseau des Clans [9 min]{.duree}

Ce sont les **alliés d'alliés**, mis de côté pendant l'atelier de la Séance 1.

- **Le modèle** : des nœuds (Joueur, Héros, Clan, Île, Trésor) et des relations qui portent un nom et des propriétés (`ALLIE_A`, `MEMBRE_DE`, `MENTOR_DE`). Une requête dessine un motif : `(c:Clan)-[:ALLIE_A*2]-(autre:Clan)`.
- **Sur Félicia** : les Clans à deux alliances du Cercle de l'Aube, le chemin diplomatique le plus court entre deux Clans, les Joueurs dont deux Héros sont dans des Clans non alliés.
- **Forces** : parcours de relations à profondeur variable, coût proportionnel à ce qu'on parcourt et non à la taille des tables.
- **Limites** : peu adapté aux agrégats massifs (« combien de Vies perdues par zone ? ») ; il ne garde que les relations qu'on y a mises.
- **Scripts** : `demonstrations/s3/4-neo4j-clans.cypher`, et la même question en SQL dans `4-postgres-alliances.sql`.

## Groupes experts et redistribution

Pendant une heure, votre groupe devient **expert d'un seul paradigme**. Il traite les Tickets du Game Designer de sa fiche dans le Codespace, puis remplit sa fiche synthèse : cas d'usage, requête type, limites. Ensuite, en groupe mixte (un expert de chaque paradigme), chacun présente le sien en 8 minutes environ, et tous complètent la fiche commune.

::: {.encadre .astuce}
Vous allez **enseigner** votre paradigme. Pendant les Tickets, notez ce qui vous a surpris ou bloqué : c'est ce que vos camarades devront entendre.
:::

## La grille de choix, construite ensemble

À 10h50, la classe remplit cette grille au tableau, à partir de ce que les experts ont présenté. Notez ici quelques mots par case, pas des phrases ; une case vide sera complétée par la grille de référence, qui vous est remise ensuite, pour le Boss et la Note 2.

::: {.remplir .libelles .grille}
| Critère | Relationnel | Document | Clé-valeur | Colonne | Graphe |
|-----------------------------|-------------|------------|------------|------------|------------|
| 1 · Structure des données | | | | | |
| 2 · Volume | | | | | |
| 3 · Latence | | | | | |
| 4 · Besoin de transactions | | | | | |
| 5 · Relations | | | | | |
:::

**« Demande au Familier »** : le formateur pose au Familier une question d'architecture sur un besoin de Félicia. Notez les écarts entre sa recommandation et la grille.

[ ]{.a-remplir}

[ ]{.a-remplir}

[ ]{.a-remplir}
