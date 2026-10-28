---
title: Atelier dénormalisation
soustitre: L'écran de profil d'un Héros, mesuré dans PostgreSQL
surtitre: Séance 2 · 9h45 à 10h20
public: Support étudiant
---

::: bloc
### Ticket du Game Designer

> « Depuis la Saison de la Lune Rousse, **l'écran de profil d'un Héros met trois secondes à s'afficher**. Les Joueurs l'ouvrent sans arrêt : avant chaque combat, après chaque Trésor obtenu. Je veux qu'il s'affiche instantanément. Vous avez carte blanche, mais je ne veux pas d'une bourse fausse à l'écran. »
>
> Le Game Designer de Griffe & Grimoire
:::

L'écran de profil affiche, pour un Héros : son nom, son Joueur, sa Lignée, son niveau, sa Renommée, son Clan, son mentor, ses **Vies restantes** dans la Saison en cours, sa **bourse de Pelotes d'or** et son **nombre de Trésors**. On l'étudie sur **Sorbet Pelage-d'Or**, le Héros n°8.

Votre base contient 518 713 mouvements de Pelotes d'or. Celle du studio en contient des centaines de millions : vos temps seront en millisecondes, pas en secondes. C'est le **rapport** entre deux temps qui compte, pas leur valeur.

## Comment travailler [35 min]{.duree}

- En binôme, ou seul si votre Codespace fonctionne : chacun note ses propres mesures.
- Les scripts sont dans le dépôt, dossier `ateliers/s2/`. Ouvrez-les dans l'éditeur du Codespace pour les lire, puis lancez-les dans le terminal :

```bash
make sql F=ateliers/s2/1-profil-jointures.sql
```

- Vous pouvez aussi copier une requête dans `make psql`. Une requête précédée de `EXPLAIN ANALYZE` affiche son **plan d'exécution** et, en dernière ligne, son temps réel : `Execution Time`.
- `make charger` remet la base dans son état d'origine si quelque chose a mal tourné.

| Étape | Script | Temps conseillé |
|--------|-----------------------------------------|---------------|
| | Lecture du Ticket et de cette fiche | 3 min |
| 1 | `1-profil-jointures.sql` : la requête d'aujourd'hui | 5 min |
| 2 | `2-profil-table.sql` et `3-profil-vue.sql` : deux copies du profil | 8 min |
| 3 | `4-coherence.sql` : ce que coûte une écriture | 7 min |
| 4 | Votre recommandation, en une phrase | 4 min |
| | Discussion collective | 8 min |

## Étape 1 · La requête multi-jointures [5 min]{.duree}

Lancez le script 1. Il affiche le profil de Sorbet, puis le **plan d'exécution** de la même requête. Ne lisez pas tout le plan : cherchez la ligne `Seq Scan on transaction_pelotes` et, juste en dessous, `Rows Removed by Filter`.

1. Relevez l'`Execution Time` (dernière ligne).
2. Combien de mouvements PostgreSQL lit-il pour n'en garder que ceux de Sorbet ? Pourquoi lit-il toute la table ?

## Étape 2 · Deux copies du profil [8 min]{.duree}

Le script 2 crée la **table dénormalisée** `profil_heros` : une ligne par Héros, avec tout ce que l'écran affiche, déjà calculé. Le script 3 construit la même chose en **vue matérialisée** (`CREATE MATERIALIZED VIEW`) : PostgreSQL retient la requête et stocke son résultat. Lancez les deux d'un coup :

```bash
make sql F=ateliers/s2/2-profil-table.sql && make sql F=ateliers/s2/3-profil-vue.sql
```

1. Pour chacune, relevez l'`Execution Time` de la lecture du profil. Combien de fois est-elle plus rapide qu'à l'étape 1 ?
2. Pour tenir la copie à jour, qu'est-ce qui distingue la vue de la table ?

## Étape 3 · Ce que coûte une écriture [7 min]{.duree}

Sorbet termine une quête et gagne 500 Pelotes d'or. Le script 4 enregistre le mouvement, compare la bourse affichée par les trois solutions, les remet à jour, puis **annule tout** : la base reste intacte.

1. Juste après la quête, quelle bourse affiche chaque solution ? Laquelle a raison ?
2. Un Héros fait des dizaines de mouvements par heure de jeu. Que faut-il faire, à chaque mouvement, pour remettre la table à jour ? Et la vue ? Relevez le temps du `REFRESH`.

## Étape 4 · Votre recommandation [4 min]{.duree}

Pour le Game Designer, en une phrase : quelle solution recommandez-vous, et à quelle condition ?

## Pour la discussion [8 min]{.duree}

- Les Vies restantes et le nombre de Trésors sont-ils aussi sensibles au retard que la bourse ?
- Vous connaissez les index depuis le B1. Ne suffirait-il pas d'en créer un ? Quand la dénormalisation reste-t-elle utile malgré l'index ?
- Le Game Designer ne veut « pas d'une bourse fausse à l'écran ». Laquelle des solutions le respecte, et à quel prix en écriture ?

Ce raisonnement, gain en lecture contre coût en cohérence et en écriture, est celui que la Note 1 vous demande pour **un** choix de dénormalisation.
