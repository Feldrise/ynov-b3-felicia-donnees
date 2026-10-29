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

L'écran de profil montre le nom du Héros, son Joueur, sa Lignée, son niveau, sa Renommée, son Clan, son mentor, ses **Vies restantes** dans la Saison en cours, sa **bourse de Pelotes d'or** et son **nombre de Trésors**. On travaille sur **Sorbet Pelage-d'Or**, le Héros n°8.

Ta base a 518 713 mouvements de Pelotes d'or, celle du studio des centaines de millions : regarde le **rapport** entre deux temps, pas leur valeur.

## Comment travailler [35 min]{.duree}

En binôme, ou en individuel si ton Codespace fonctionne : chacun note ses mesures. Les scripts sont dans `ateliers/s2/` : lis-les dans l'éditeur, lance-les dans le terminal.

```bash
make sql F=ateliers/s2/1-profil-jointures.sql
```

Dans `make psql`, une requête précédée de `EXPLAIN ANALYZE` affiche son **plan d'exécution** et, en dernière ligne, son `Execution Time`. En cas de pépin, `make charger` remet la base d'origine.

Lecture (3 min), étapes 1 à 4 (5, 8, 7 et 4 min), discussion collective (8 min).

## Étape 1 · La requête multi-jointures [5 min]{.duree}

Le script 1 (la commande ci-dessus) affiche le profil de Sorbet, puis son **plan d'exécution**. Cherchez juste `Seq Scan on transaction_pelotes` et, en dessous, `Rows Removed by Filter`.

1. Relevez l'`Execution Time` (dernière ligne).
2. Combien de mouvements PostgreSQL lit-il pour n'en garder que ceux de Sorbet ? Pourquoi lit-il toute la table ?

## Étape 2 · Deux copies du profil [8 min]{.duree}

Le script 2 crée la **table dénormalisée** `profil_heros`, une ligne par Héros, tout l'écran déjà calculé. Le script 3 fait pareil en **vue matérialisée** : PostgreSQL retient la requête et stocke son résultat. Lancez les deux :

```bash
make sql F=ateliers/s2/2-profil-table.sql && make sql F=ateliers/s2/3-profil-vue.sql
```

1. Pour chacune, relevez l'`Execution Time` de la lecture du profil. Combien de fois plus rapide qu'à l'étape 1 ?
2. Pour tenir la copie à jour, qu'est-ce qui distingue la vue de la table ?

## Étape 3 · Ce que coûte une écriture [7 min]{.duree}

Sorbet gagne 500 Pelotes d'or en quête. Le script 4, `4-coherence.sql`, enregistre le mouvement, compare la bourse des trois solutions, les remet à jour, puis **annule tout** : la base reste intacte.

1. Juste après la quête, quelle bourse affiche chaque solution ? Laquelle a raison ?
2. Un Héros fait des dizaines de mouvements par heure. Que faut-il faire, à chaque mouvement, pour remettre la table à jour ? Et la vue ? Relevez le temps du `REFRESH`.

## Étape 4 · Votre recommandation [4 min]{.duree}

En une phrase, pour le Game Designer : quelle solution, et à quelle condition ?

## Pour la discussion [8 min]{.duree}

- Les Vies restantes et le nombre de Trésors sont-ils aussi sensibles au retard que la bourse ?
- Vous connaissez les index depuis le B1. Un index ne suffirait-il pas ? Quand la dénormalisation reste-t-elle utile malgré lui ?
- Le Game Designer ne veut « pas d'une bourse fausse à l'écran ». Laquelle des solutions le respecte, et à quel prix en écriture ?

Gain en lecture contre coût en cohérence et en écriture : c'est le raisonnement que la Note 1 te demandera, pour **un** choix.
