---
title: Du MCD au MPD
soustitre: Normaliser, puis dénormaliser à bon escient
surtitre: Séance 2 · Mardi 10 novembre, 8h00 à 12h00
public: Support étudiant
---

## Au programme

Bug Hunt n°2 (15 min), du MCD au MLD puis au MPD (35 min), formes normales et exercice éclair (25 min), ton Codespace (20 min), pause (10 min), atelier dénormalisation (35 min), consignes de la Note 1 (10 min), **Note 1** (1 h 15), préparation de la Note 2 (15 min).

Garde sous la main ton MCD de Félicia de la Séance 1, ou celui du tableau.

## 1. Bug Hunt n°2 : la table « Inventaire » [15 min]{.duree}

Le sac d'un Héros a **30 emplacements**, chacun avec au plus un Trésor. Le studio exporte tout dans `INVENTAIRE` : **une ligne par emplacement, vide ou occupé**, de clé **(id_heros, num_emplacement)**.

![La table « Inventaire », telle que l'outil du studio l'exporte](bug-hunt-2.svg){width=200px}

Un extrait, coupé en trois (la clé est répétée à chaque fois) :

::: compact
| id_heros | num_emplacement | nom_heros | pseudo_joueur | courriel_joueur |
|----|-----------|----------------------|----------------|-------------------------|
| 7 | 1 | Topaze Herbe-Folle | kawa_ronron593 | kawa_ronron593@felicia.test |
| 7 | 2 | Topaze Herbe-Folle | kawa_ronron593 | kawa_ronron593@felicia.test |
| 8 | 1 | Sorbet Pelage-d'Or | kawa_ronron593 | kawa_ronron593@felicia.test |
| 8 | 2 | Sorbet Pelage-d'Or | kawa_ronron593 | kawa_ronron593@felicia.test |
| 8 | 3 | Sorbet Pelage-d'Or | kawa_ronron593 | kawa_ronron593@felicia.test |
| 8 | 4 | Sorbet Pelage-d'Or | kawa_ronron593 | kawa_ronron593@felicia.test |

| id_heros | num_emplacement | id_clan | nom_clan | id_tresor | nom_tresor |
|----|----|----|-----------------------------|----|---------------------------|
| 7 | 1 | 15 | Les Chasseurs du Crépuscule | 9 | Heaume des Marées |
| 7 | 2 | 15 | Les Chasseurs du Crépuscule | |  |
| 8 | 1 | 78 | Le Cercle du Velours | 14 | Sabre courbe d'Opale |
| 8 | 2 | 78 | Le Cercle du Velours | 17 | Plume de phénix de Brume |
| 8 | 3 | 78 | Le Cercle du Velours | 18 | Fiole d'Ébène |
| 8 | 4 | 78 | Le Cercle du Velours | 19 | Médaillon de Brume |

| id_heros | num_emplacement | nature | rareté | enchantements | date_rangement |
|----|----|---------|--------|---------------------|------------------|
| 7 | 1 | armure | épique | givre, lune | 2026-10-02 18:40 |
| 7 | 2 |  |  |  |  |
| 8 | 1 | arme | rare | lune, foudre, givre | 2026-10-21 09:12 |
| 8 | 2 | relique | rare |  | 2026-10-30 22:47 |
| 8 | 3 | potion | rare |  | 2026-11-05 07:58 |
| 8 | 4 | parure | rare | feu | 2026-11-06 12:31 |
:::

::: bloc
### En binôme, 9 minutes

La table cache **sept anomalies**. Trouvez-en **au moins quatre** et dites, pour chacune, de quoi dépend vraiment la colonne fautive : une colonne à plusieurs valeurs, une colonne qui ne dépend que d'une partie de la clé, ou d'une autre colonne non clé. La correction fera le reste.
:::

Gardez votre liste, le bloc 3 en part.

## 2. Du MCD au MLD, puis au MPD [35 min]{.duree}

On part du **MCD corrigé de Félicia**. Le MLD dit quelles tables et quelles clés ; le MPD, comment un SGBD précis les stocke.

### Les règles de passage

| Dans le MCD | Dans le MLD | Sur Félicia |
|---------------------------|-----------------------------------------------|----------------------------------|
| Une entité | une table, l'identifiant devient clé primaire | JOUEUR (<u>id_joueur</u>, pseudo, ...) |
| Une patte **1,1** (ou **0,1**) | pas de table : la clé d'en face migre en **clé étrangère** (facultative en 0,1), avec les attributs de l'association | INCARNER : *#id_joueur* dans HÉROS ; APPARTENIR : *#id_clan* et date_adhesion dans HÉROS |
| Une association **0,N / 0,N** (ou 1,N) | une table, clé = les clés reliées, attributs de l'association compris | ALLIER (<u>*#id_clan_premier*, *#id_clan_second*</u>, date_alliance) |
| Une **ternaire** | une table à trois clés, sauf patte 1,1 : cas précédent | OBTENIR migre dans TRÉSOR |
| Une **réflexive** | même règle, les **rôles** nomment les colonnes | *#id_heros_mentor* dans HÉROS |
| Une **identification relative** (_11) | la clé de l'entité forte entre dans celle de la faible | ZONE (<u>*#id_ile*, nom_zone</u>) |

Le **MLD de Félicia**, tel que Looping ou Mocodo le génère :

::: compact
- **JOUEUR** (<u>id_joueur</u>, pseudo, courriel, pays, date_inscription)
- **HÉROS** (<u>id_heros</u>, nom_heros, niveau, date_creation, *#id_joueur*, *#id_heros_mentor*, date_debut_mentorat, *#id_clan*, date_adhesion, est_sorcier, élément, est_rodeur_d_ombre, furtivité, est_gardien, rempart, est_alchimiste, recettes_connues)
- **CLAN** (<u>id_clan</u>, nom_clan, devise, date_fondation, *#id_heros_chef*, *#id_ile*)
- **ALLIER** (<u>*#id_clan_premier*, *#id_clan_second*</u>, date_alliance)
- **ÎLE** (<u>id_ile</u>, nom_ile)
- **ZONE** (<u>*#id_ile*, nom_zone</u>)
- **SAISON** (<u>id_saison</u>, nom_saison)
- **TRÉSOR** (<u>id_tresor</u>, nom_tresor, nature, rareté, *#id_heros_propriétaire*, *#id_heros*, *#id_ile*, date_obtention)
- **POSSESSION_TRÉSOR** (<u>*#id_tresor*, date_debut</u>, date_fin, *#id_heros*)
- **VIE_PERDUE** (<u>id_vie</u>, numéro, date_heure, cause, *#id_heros*, *#id_heros_vainqueur*, *#id_ile*, *#nom_zone*, *#id_saison*)
:::

### L'héritage : trois façons de traduire les Lignées

Le MCD ne bouge pas, mais le MLD a trois façons de traduire un héritage.

![Le fragment des Lignées, repris de la Séance 1](heritage-table-unique.svg){width=520px}

| Stratégie | Gagne | Paie |
|----------------------|-------------------------------|------------------------------------|
| **Une seule table** : HÉROS absorbe les filles | aucune jointure | des colonnes vides ; le XT ne tient que par des `CHECK` |
| **Une table par entité** : HÉROS, SORCIER (<u>*#id_heros*</u>, élément)... | aucune colonne vide | une jointure pour lire un Héros complet ; rien n'empêche un Héros Sorcier et Gardien |
| **Les filles seulement** : SORCIER (<u>id_heros</u>, nom_heros, niveau, élément)... | une Lignée se lit d'un bloc | « tous les Héros » = une union de quatre tables ; possible seulement si l'héritage est total (T) |

La base de Félicia a pris **une seule table**, des `CHECK`, et une colonne `id_lignee` vers une petite table LIGNÉE.

### Démonstration : générer, puis relire

Je génère devant vous le MLD et le SQL dans Looping. Ce n'est qu'**un premier jet** : l'outil ne connaît pas tes règles de gestion. Relis-le avec cette grille, ici comme à la Note 1.

::: bloc
### Relire un MLD généré : huit questions

1. Chaque clé primaire identifie-t-elle vraiment une ligne ?
2. Chaque clé étrangère dit-elle son **rôle** (`id_heros_proprietaire`) ?
3. Les colonnes obligatoires sont-elles `NOT NULL` ?
4. Les règles chiffrées sont-elles en `CHECK` (niveau de 1 à 60, Vie de 1 à 9) ?
5. Les unicités du métier sont-elles en `UNIQUE` (une seule Vie n°3 par Saison) ?
6. L'héritage est-il traduit comme décidé, exclusion comprise ?
7. Une clé composée mérite-t-elle une clé technique (`id_zone`) ?
8. Ce qu'on filtre ou joint souvent a-t-il un **index** ? PostgreSQL n'indexe pas les clés étrangères tout seul.
:::

### Du MLD au MPD : la base de Félicia

Le MPD, c'est le script vraiment chargé dans PostgreSQL, `bases/postgres/schema.sql`. Compare-le au MLD généré : types choisis, règles de gestion en contraintes, quelques choix du MLD revus.

```sql
CREATE TABLE vie_perdue (
  id_vie              INTEGER PRIMARY KEY,
  id_heros            INTEGER NOT NULL,
  id_saison           SMALLINT NOT NULL,
  numero              SMALLINT NOT NULL CHECK (numero BETWEEN 1 AND 9),  -- les 9 Vies
  date_heure          TIMESTAMPTZ NOT NULL,
  id_zone             SMALLINT NOT NULL,             -- plutôt que (id_ile, nom_zone)
  cause               VARCHAR(30) NOT NULL,
  id_heros_vainqueur  INTEGER,
  UNIQUE (id_heros, id_saison, numero),              -- une seule Vie n°3 par Saison
  CHECK ((cause = 'duel') = (id_heros_vainqueur IS NOT NULL))  -- vainqueur en duel
);
```

Il contient aussi `transaction_pelotes`, un mouvement de **Pelotes d'or** par ligne : plus de 500 000 lignes, **aucun index** sur `id_heros`. On y revient à l'atelier.

## 3. Formes normales [25 min]{.duree}

Une **dépendance fonctionnelle** A → B : connaître A suffit pour connaître B (`id_clan → nom_clan`).

| Forme | Règle | Ce qu'elle évite |
|------|-------------------------------------------------------|------------------------------------------|
| **1FN** | une valeur atomique par colonne, une clé | une valeur noyée dans une liste |
| **2FN** | 1FN, et tout dépend de **toute** la clé | la même info sur chaque ligne d'un Héros |
| **3FN** | 2FN, et rien ne dépend d'une **colonne non clé** | la même info sur chaque ligne d'un Clan ou d'un Trésor |

Pour corriger, on **sort** la colonne fautive dans une nouvelle table, avec ce dont elle dépend, qui en devient la clé et reste en clé étrangère dans l'originale.

### Normalisation pas à pas de l'Inventaire

Ensemble, au tableau, à partir de vos listes. Note les tables à chaque étape.

::: {.remplir .libelles}
| Étape | Tables obtenues |
|---------|------------------------------------------------------------------------|
| 1FN | |
| 2FN | |
| 3FN | |
:::

### Exercice éclair, en binôme [13 min]{.duree} {.nouvelle-page}

Le studio exporte les Vies perdues dans une seule table, de clé **(id_heros, id_saison, numéro)**.

::: {.compact .etroit}
| id_heros | id_saison | numéro | nom_heros | nom_saison | date_heure | id_zone | nom_zone | nom_ile |
|----|----|----|--------------------|--------------------------|------------------|----|----------------------|--------------|
| 8 | 4 | 1 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-10-14 23:24 | 20 | Marché Flottant | Grand-Ronron |
| 8 | 4 | 2 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-11-05 08:11 | 22 | Bibliothèque Volante | Grand-Ronron |
| 8 | 4 | 3 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-11-07 02:27 | 22 | Bibliothèque Volante | Grand-Ronron |
| 272 | 4 | 7 | Ibis le Pensif | Saison de la Lune Rousse | 2026-11-08 22:26 | 22 | Bibliothèque Volante | Grand-Ronron |
:::

1. Écrivez au moins trois dépendances fonctionnelles qui ne partent pas de la clé complète.
2. La table est-elle en 2FN ? Sinon, décomposez-la.
3. Le résultat est-il en 3FN ? Sinon, décomposez encore. Écrivez les tables finales en MLD : clés soulignées, clés étrangères en #.

Le Familier est autorisé : vérifiez ses dépendances sur l'extrait.

## 4. Mise en place de l'environnement [20 min]{.duree}

Suis le guide **Ouvrir son Codespace** (sur Moodle). Au premier repère horaire dépassé, lève la main.

C'est prêt quand `make etat` montre cinq bases **healthy** et que `SELECT count(*) FROM heros;` renvoie **7013**.

## 5. Pause [10 min]{.duree}

## 6. Atelier dénormalisation [35 min]{.duree}

Tout est dans la fiche **Atelier dénormalisation**, distribuée au début du bloc.

## 7. Consignes de la Note 1 [10 min]{.duree}

Je vous présente le document **Consignes de la Note 1**, sur Moodle.

## 8. Note 1 [1 h 15]{.duree}

En individuel. Le sujet est distribué à 10h30.

## 9. Préparation de la Note 2 [15 min]{.duree}

On forme les trinômes, et chaque groupe tire au sort son **Sujet de Note 2**. Vous en prenez juste connaissance : rien à faire avant la Séance 3.

::: bloc
### À retenir de la Séance 2

- Le MLD se **déduit** du MCD par des règles. Un outil les applique, mais relis toujours ce qu'il génère.
- L'héritage a **trois** traductions. Choisir, c'est arbitrer entre colonnes vides, jointures et garanties.
- 1FN : pas de liste dans une colonne. 2FN : tout dépend de toute la clé. 3FN : rien ne dépend d'une colonne non clé.
- Dénormaliser, c'est **recopier** pour lire plus vite : pour une charge précise, mesuré, avec quelqu'un qui maintient la copie.
:::

En partant, **arrête ton Codespace** (fin du guide) : tu le rouvriras en Séance 3.
