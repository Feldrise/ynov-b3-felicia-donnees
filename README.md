# Neuf Vies : Les Îles de Félicia

Dépôt du module « Conception architecture des données » (Bachelor 3 Informatique, Ynov).

Ce dépôt contient les cinq bases de données du Fil rouge, *Neuf Vies : Les Îles de Félicia*, un action-RPG en ligne édité par le studio Griffe & Grimoire, et le jeu de données qui va avec : des Joueurs, leurs Héros (des chats-mages), leurs Lignées, leurs Clans, leurs Trésors, leurs Pelotes d'or et les Vies qu'ils perdent, à raison de 9 par Saison.

## Démarrer

Ouvrez ce dépôt dans un **Codespace** (bouton **Code**, onglet **Codespaces**), puis dans le terminal :

```bash
make up      # démarre les cinq bases et charge le jeu de données (1 à 2 minutes)
make etat    # vérifie que tout est prêt
make psql    # ouvre un terminal SQL sur PostgreSQL
```

Le guide pas à pas, avec la procédure de secours, est sur Moodle : « Ouvrir son Codespace ».

Avec Docker déjà installé sur votre ordinateur, les mêmes commandes fonctionnent à la racine du dépôt (sous Windows, depuis WSL).

## Les commandes

`make aide` les liste toutes. Les principales :

| Commande | Effet |
|---|---|
| `make up` | Démarre les bases et charge le jeu de données. |
| `make etat` | Affiche l'état des bases et un effectif par base. |
| `make psql`, `make mongosh`, `make redis-cli`, `make cqlsh`, `make cypher-shell` | Ouvre le terminal de PostgreSQL, MongoDB, Redis, Cassandra ou Neo4j. |
| `make charger` | Recharge le jeu de données d'origine. |
| `make down` | Arrête et détruit les bases. |

## Ce que contient chaque base

| Base | Ce que vous y trouvez |
|---|---|
| PostgreSQL | Le modèle relationnel complet de Félicia (`bases/postgres/schema.sql`). |
| MongoDB | Les Héros, les Clans et les Trésors, dont les attributs varient selon leur nature. |
| Redis | Le classement de la Saison en cours, les Vies restantes et la bourse de chaque Héros. |
| Cassandra | La télémétrie des Vies perdues, par Héros et par Île. |
| Neo4j | Le réseau des Joueurs, des Héros, des Clans et de leurs alliances. |

Le jeu de données est généré par `donnees/generer.py` : tout le monde obtient exactement les mêmes données, avec les mêmes identifiants dans les cinq bases.
