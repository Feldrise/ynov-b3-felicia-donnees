---
title: Groupe expert colonne
soustitre: La télémétrie des Vies perdues dans Cassandra, quatre Tickets du Game Designer guidés
surtitre: Séance 3 · Groupes experts, 9h10 à 10h10
public: Support étudiant
---

## Votre heure

::: bloc
| Quand | Quoi |
|---------------|--------------------------------------------------------------|
| 9h10 [5 min]{.duree} | Codespace ouvert, bases démarrées (`make etat`), terminal Cassandra ouvert, lecture de la fiche |
| 9h15 [35 min]{.duree} | Tickets 1 à 4, chacun sur son Codespace, en s'entraidant ; le Ticket bonus si vous avez fini |
| 9h50 [15 min]{.duree} | fiche synthèse du groupe : cas d'usage, requête type, limites |
| 10h05 [5 min]{.duree} | chacun répète à voix haute le début de sa présentation de 8 minutes |
:::

Ouvrez le terminal Cassandra avec `make cqlsh`. Pour sortir : `exit`. Chaque requête se termine par un point-virgule ; les `___` sont à remplacer.

::: encadre
### Rappel du modèle

Deux tables rangent les mêmes Vies perdues pour deux questions différentes.

- `vies_par_ile` : clé de partition `(id_ile, id_saison)`, puis rangée par `zone`, `date_heure`, `id_heros`, `numero`. Autres colonnes : `cause`, `id_clan`.
- `vies_par_heros` : clé de partition `(id_heros, id_saison)`, rangée par `numero`. Autres colonnes : `date_heure`, `ile`, `zone`, `cause`, `id_heros_vainqueur`.

Une requête doit donner **toute** la clé de partition, avec `=` ou `IN`. Les Îles : 1 Brume, 2 Velours, 3 Croc-de-Pierre, 4 Lune-Rousse, 5 Ronces, 6 Cendres, 7 Grand-Ronron, 8 Nuit-Sans-Fin. La Saison en cours est la 4. `DESCRIBE TABLE vies_par_ile;` affiche une table.
:::

## Ticket 1 · Où les Héros perdent-ils le plus de Vies sur l'Île de Brume ? [6 min]{.duree}

> « L'Île de Brume a mauvaise réputation. Où y perd-on le plus de Vies, et est-ce pareil à chaque Saison ? »
> — le studio

La démonstration a compté les Vies perdues par zone pour la Saison en cours. Faites-le pour les quatre Saisons en une seule requête : `IN` donne plusieurs partitions, et le regroupement doit alors commencer par la Saison.

```sql
SELECT id_saison, zone, count(*) FROM vies_par_ile WHERE id_ile = ___ AND id_saison IN (___) GROUP BY id_saison, zone;
```

**Pour vérifier** : 16 lignes, quatre zones pour chacune des quatre Saisons.

**Pour la fiche** : combien de partitions cette requête a-t-elle lues ? Dans un vrai cluster, sur combien de serveurs peuvent-elles se trouver ?

## Ticket 2 · Le journal de Gribouille, endormi [8 min]{.duree}

> « Gribouille Rôde-Toits (Héros 1254) a perdu ses 9 Vies cette Saison. Son Joueur conteste. Sortez-nous son journal, puis seulement les Vies perdues en duel. »
> — le studio

1. Le journal complet de la Saison :

```sql
SELECT numero, date_heure, ile, zone, cause, id_heros_vainqueur FROM vies_par_heros WHERE id_heros = ___ AND id_saison = ___;
```

2. Seulement les duels. Essayez d'abord sans la fin de la ligne, lisez le message d'erreur, puis ajoutez-la :

```sql
SELECT numero, zone, id_heros_vainqueur FROM vies_par_heros WHERE id_heros = 1254 AND id_saison = 4 AND cause = 'duel' ALLOW FILTERING;
```

**Pour vérifier** : 9 lignes, puis 5.

**Pour la fiche** : `ALLOW FILTERING` est acceptable ici. Pourquoi ? Pourquoi ne l'est-il plus sur toute la table, comme à la fin de la démonstration ?

## Ticket 3 · Les dernières Vies perdues au Marais Sans Fond [7 min]{.duree}

> « Un bug de collision est signalé au Marais Sans Fond, sur l'Île de Brume. Montrez-nous les cinq dernières Vies perdues là-bas cette Saison, de la plus récente à la plus ancienne. »
> — le studio

```sql
SELECT date_heure, id_heros, cause FROM vies_par_ile WHERE id_ile = 1 AND id_saison = 4 AND zone = '___' ORDER BY zone DESC, date_heure DESC LIMIT ___;
```

**Pour vérifier** : cinq lignes, dates décroissantes.

**Pour la fiche** : essayez `ORDER BY cause`. Pourquoi l'ordre des lignes est-il décidé **à la création de la table** ?

## Ticket 4 · Une table pour une nouvelle question [12 min]{.duree}

> « L'équilibrage veut suivre, journée par journée, le nombre de Vies perdues pour chaque cause (chute dans le vide, sortilège, duel...), sur tout l'archipel. »
> — le studio

Aucune des deux tables ne répond : en Cassandra, on crée une table pour la question.

1. Choisissez la clé de partition : ce que la question donne toujours (une cause, une journée). Rangez ensuite par heure.

```sql
CREATE TABLE IF NOT EXISTS vies_par_cause (cause text, journee date, date_heure timestamp, id_heros int, numero int, ile text, zone text, PRIMARY KEY ((___, ___), date_heure, id_heros, numero));
```

2. Félicia écrit maintenant chaque Vie perdue dans trois tables. Ajoutez-en une à la main : la deuxième Vie de la Saison de Moustique le Gourmand (Héros 3426), perdue en duel ce matin au Phare Éteint :

```sql
INSERT INTO vies_par_cause (cause, journee, date_heure, id_heros, numero, ile, zone) VALUES ('duel', '2026-11-13', '2026-11-13 09:30:00+0000', 3426, 2, 'Brume', 'Phare Éteint');
```

3. Comptez les duels du 13 novembre avec `SELECT count(*) FROM vies_par_cause WHERE ...;` : vous devez obtenir 1.
4. Remettez la base en état : `DROP TABLE IF EXISTS vies_par_cause;`.

**Pour la fiche** : pourquoi pas une partition par cause seule ? Pensez à la taille de la partition « chute dans le vide » au bout de deux ans.

## Ticket bonus · Le coût de la double écriture

> « Une Vie perdue est maintenant écrite dans trois tables. Que se passe-t-il si l'écriture réussit dans deux tables et échoue dans la troisième ? »
> — le studio

Relisez l'étape 5 du script `demonstrations/s3/3-cassandra-telemetrie.cql` (`BEGIN BATCH`) et expliquez ce qu'elle garantit, et ce qu'elle ne garantit pas par rapport à une transaction PostgreSQL.

## Votre fiche synthèse [15 min]{.duree}

Remplissez la fiche synthèse (document à part) : deux cas d'usage sur Félicia, une requête type que vous savez expliquer, deux forces, deux limites, et un besoin pour lequel vous **ne** choisiriez **pas** la colonne. C'est votre support pour les 8 minutes de la redistribution.
