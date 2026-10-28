---
title: Du MCD au MPD
soustitre: Normaliser, puis dénormaliser à bon escient
surtitre: Séance 2 · Mardi 10 novembre, 8h00 à 12h00
public: Support étudiant
---

## Le programme de la Séance

| Heure | Bloc | Durée |
|---------------|------------------------------------------------------|---------|
| 8h00 | Bug Hunt n°2 : la table « Inventaire » | 15 min |
| 8h15 | Apport et démonstration : du MCD au MLD, puis au MPD | 35 min |
| 8h50 | Formes normales, et exercice éclair en binôme | 25 min |
| 9h15 | Mise en place de l'environnement : votre Codespace | 20 min |
| 9h35 | Pause | 10 min |
| 9h45 | Atelier dénormalisation : l'écran de profil d'un Héros | 35 min |
| 10h20 | Consignes de la Note 1 | 10 min |
| 10h30 | Note 1, en individuel | 1 h 15 |
| 11h45 | Préparation de la Note 2 : trinômes et tirage des sujets | 15 min |

Rien n'est à préparer ni à installer avant : tout se fait pendant la Séance. Gardez sous la main le MCD de Félicia de la Séance 1 (le vôtre, ou celui projeté au tableau).

## 1. Bug Hunt n°2 : la table « Inventaire » [15 min]{.duree}

Le sac de chaque Héros compte **30 emplacements numérotés** ; chaque emplacement contient au plus un Trésor. Pour suivre les sacs, l'outil interne du studio exporte une seule grande table, `INVENTAIRE`, avec **une ligne par emplacement, vide ou occupé**. Sa clé est le couple **(id_heros, num_emplacement)**.

![La table « Inventaire », telle que l'outil du studio l'exporte](bug-hunt-2.svg){width=200px}

Un extrait de ses lignes, coupé en trois pour tenir sur la page (les deux premières colonnes, la clé, sont répétées) :

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

La table fonctionne, mais elle se répète : elle contient **sept anomalies**. En 9 minutes, repérez-en **au moins quatre** et, pour chacune, dites de quoi dépend vraiment la colonne fautive :

- une colonne qui contient **plusieurs valeurs** à la fois ;
- des colonnes qui ne dépendent que d'**une partie de la clé** ;
- des colonnes qui dépendent d'une **autre colonne non clé**.

Vous n'aurez pas le temps de toutes les trouver, et ce n'est pas attendu : la correction collective complète votre liste, et c'est elle qui imagine ce qui se passe quand on **modifie** (un Clan change de nom), quand on **insère** (un Trésor obtenu mais pas encore rangé) et quand on **supprime** (on vide un emplacement).
:::

Notez vos réponses : la normalisation pas à pas du bloc 3 part de votre liste.

## 2. Du MCD au MLD, puis au MPD [35 min]{.duree}

On part du **MCD corrigé de Félicia**, celui de la Séance 1. Trois niveaux, trois questions :

| Niveau | Question | Ce qu'on y voit |
|---------------|------------------------------------------|----------------------------------------------|
| MCD (conceptuel) | De quoi parle-t-on ? | entités, associations, cardinalités, règles de gestion |
| MLD (logique) | Quelles tables, quelles clés ? | tables, clés primaires, clés étrangères (#) |
| MPD (physique) | Comment le SGBD le stocke-t-il ? | types, `NOT NULL`, `UNIQUE`, `CHECK`, index, dans un SGBD précis |

### Les règles de passage du MCD au MLD

| Dans le MCD | Dans le MLD | Sur Félicia |
|---------------------------------------|-----------------------------------------------|----------------------------------|
| Une entité | une table ; son identifiant devient la clé primaire | JOUEUR (<u>id_joueur</u>, pseudo, ...) |
| Une association avec une patte **1,1** (ou **0,1**) | pas de table : la clé de l'autre entité migre comme **clé étrangère** du côté 1,1 (ou 0,1, colonne facultative) | INCARNER : HÉROS reçoit *#id_joueur* ; APPARTENIR : HÉROS reçoit *#id_clan*, facultatif |
| Une association **0,N / 0,N** (ou 1,N) | une table, dont la clé réunit les clés des entités reliées ; les attributs de l'association y vont | ALLIER (<u>*#id_clan_premier*, *#id_clan_second*</u>, date_alliance) |
| Une association **ternaire** | une table dont la clé réunit les trois clés... sauf si une patte est 1,1 : on se ramène alors au cas 1,1 | OBTENIR : la patte 1,1 du Trésor fait migrer *#id_heros*, *#id_ile* et la date dans TRÉSOR |
| Une association **réflexive** | même règle, les **rôles** nomment les deux colonnes | MENTORER : HÉROS reçoit *#id_heros_mentor* et date_debut_mentorat |
| Une **identification relative** (_11) | la clé de l'entité « forte » entre dans la clé de l'entité « faible » | ZONE (<u>*#id_ile*, nom_zone</u>) |

Le **MLD de Félicia** que l'on obtient, tel que Looping ou Mocodo le génère :

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

Le MCD dit « un Héros est d'une seule Lignée, et chaque Lignée a son attribut propre » (héritage **XT** : exclusion et totalité). Le MLD peut le traduire de trois façons ; le MCD, lui, ne change pas.

![Le fragment des Lignées, repris de la Séance 1](heritage-table-unique.svg){width=520px}

| Stratégie | MLD obtenu | Gagne | Paie |
|----------------------|------------------------------------|-------------------------------|------------------------------------|
| **Une seule table** (la mère absorbe les filles) | HÉROS (<u>id_heros</u>, nom_heros, niveau, est_sorcier, élément, est_rodeur_d_ombre, furtivité, ...) | aucune jointure ; une Lignée de plus = une colonne | colonnes vides ; le XT n'est garanti que par des `CHECK` à écrire soi-même |
| **Une table par entité** (mère et filles) | HÉROS (<u>id_heros</u>, nom_heros, niveau) ; SORCIER (<u>*#id_heros*</u>, élément) ; ... | aucune colonne vide ; chaque attribut propre est `NOT NULL` | une jointure pour lire un Héros complet ; rien n'empêche un Héros d'être à la fois Sorcier et Gardien |
| **Les filles seulement** (elles absorbent la mère) | SORCIER (<u>id_heros</u>, nom_heros, niveau, élément) ; GARDIEN (...) ; ... | une Lignée se lit d'un bloc | « tous les Héros » = une union de quatre tables ; un `id_heros` unique entre quatre tables est à garantir à la main ; seulement possible si l'héritage est total (T) |

La base de Félicia a choisi **une seule table** : on lit un Héros sans jointure, et des `CHECK` garantissent qu'un Sorcier, et lui seul, a un élément. Au lieu de quatre booléens, elle range la Lignée dans une colonne `id_lignee` qui pointe vers une petite table LIGNÉE, avec son nom et sa description.

### Démonstration : générer le MLD et le script SQL, puis les relire

Le formateur ouvre le MCD de Félicia dans Looping, génère le MLD puis le script SQL pour PostgreSQL. Un MLD généré est **un premier jet** : l'outil applique les règles de passage, il ne connaît pas vos règles de gestion. Relisez-le avec cette grille, à la démonstration comme à la Note 1.

::: bloc
### Relire un MLD généré : huit questions

1. Chaque table a-t-elle une clé primaire qui identifie vraiment une ligne ?
2. Chaque clé étrangère a-t-elle un nom qui dit son **rôle** (`id_heros_proprietaire`, pas `id_heros` deux fois) ?
3. Les colonnes obligatoires sont-elles `NOT NULL` ? Un générateur laisse souvent tout facultatif.
4. Les règles de gestion chiffrées sont-elles là (`CHECK`) : niveau de 1 à 60, Vie numérotée de 1 à 9 ?
5. Les unicités du métier sont-elles là (`UNIQUE`) : un seul numéro 3 par Héros et par Saison ?
6. L'héritage est-il traduit comme vous l'avez décidé, et l'exclusion est-elle garantie ?
7. Une clé composée a-t-elle un bon candidat technique (`id_zone` plutôt que le couple île et nom) ?
8. Les colonnes que l'on filtre ou que l'on joint souvent ont-elles un **index** ? PostgreSQL n'indexe pas les clés étrangères tout seul.
:::

### Du MLD au MPD : la base de Félicia

Le MPD est le script réellement chargé dans PostgreSQL : `bases/postgres/schema.sql`, dans le dépôt du module. Comparez-le au MLD généré : les types sont choisis (`SMALLINT`, `TIMESTAMPTZ`, `JSONB` pour les attributs variables des Trésors), les règles de gestion deviennent des contraintes, et certains choix du MLD sont revus.

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

Le MPD ajoute aussi ce que le MCD ignore : les mouvements de **Pelotes d'or**, dans la table `transaction_pelotes` (un mouvement par ligne, gain ou dépense). Elle compte plus de 500 000 lignes, et **aucun index** sur `id_heros`. Vous la retrouverez dans l'atelier.

## 3. Formes normales [25 min]{.duree}

Une **dépendance fonctionnelle** A → B se lit « connaître A suffit pour connaître B » : `id_clan → nom_clan`.

| Forme | Règle | Anomalie qu'elle supprime |
|------|-------------------------------------------------------|------------------------------------------|
| **1FN** | chaque colonne contient une valeur atomique, sans liste ni groupe répété ; la table a une clé | on ne peut ni chercher ni contraindre une valeur noyée dans une liste |
| **2FN** | 1FN, et chaque colonne non clé dépend de **toute** la clé, pas d'une partie | la même information répétée sur chaque ligne d'un même Héros |
| **3FN** | 2FN, et aucune colonne non clé ne dépend d'une **autre colonne non clé** | la même information répétée sur chaque ligne d'un même Clan ou d'un même Trésor |

La méthode, sur chaque anomalie : on **sort** la colonne fautive dans une nouvelle table, avec la colonne dont elle dépend vraiment, qui en devient la clé ; dans la table d'origine, cette colonne reste comme clé étrangère.

### Normalisation pas à pas de l'Inventaire

Au tableau, avec la salle, à partir de votre liste du Bug Hunt : 1FN, puis 2FN, puis 3FN. Notez les tables obtenues à chaque étape.

::: {.remplir .libelles}
| Étape | Tables obtenues |
|---------|------------------------------------------------------------------------|
| 1FN | |
| 2FN | |
| 3FN | |
:::

### Exercice éclair, en binôme [13 min]{.duree} {.nouvelle-page}

L'équipe d'analyse du studio exporte les Vies perdues dans une seule table. Clé : **(id_heros, id_saison, numéro)**.

::: {.compact .etroit}
| id_heros | id_saison | numéro | nom_heros | nom_saison | date_heure | id_zone | nom_zone | nom_ile |
|----|----|----|--------------------|--------------------------|------------------|----|----------------------|--------------|
| 8 | 4 | 1 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-10-14 23:24 | 20 | Marché Flottant | Grand-Ronron |
| 8 | 4 | 2 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-11-05 08:11 | 22 | Bibliothèque Volante | Grand-Ronron |
| 8 | 4 | 3 | Sorbet Pelage-d'Or | Saison de la Lune Rousse | 2026-11-07 02:27 | 22 | Bibliothèque Volante | Grand-Ronron |
| 272 | 4 | 7 | Ibis le Pensif | Saison de la Lune Rousse | 2026-11-08 22:26 | 22 | Bibliothèque Volante | Grand-Ronron |
:::

1. Écrivez les dépendances fonctionnelles qui ne partent pas de la clé complète (au moins trois).
2. La table est-elle en 2FN ? Sinon, décomposez-la.
3. Le résultat est-il en 3FN ? Sinon, décomposez encore. Vos tables finales sont le MLD : clés soulignées, clés étrangères marquées #, sans recopier deux fois la même chose.

Le Familier est autorisé ; si vous le sollicitez, vérifiez ses dépendances une par une sur l'extrait.

## 4. Mise en place de l'environnement [20 min]{.duree}

Suivez le guide **Ouvrir son Codespace**, déposé sur Moodle. Il prévoit quatre étapes et un repère horaire pour chacune, puis une procédure de secours : au premier repère dépassé, levez la main.

C'est prêt quand `make etat` montre cinq bases **healthy** et que `SELECT count(*) FROM heros;` renvoie **7013**.

## 5. Pause [10 min]{.duree}

## 6. Atelier dénormalisation [35 min]{.duree}

Le Ticket du Game Designer, les scripts et les questions sont dans la fiche **Atelier dénormalisation**, distribuée au début du bloc. Vous mesurez vous-même, dans votre Codespace, ce que l'on gagne en lecture et ce que l'on paie en cohérence.

## 7. Consignes de la Note 1 [10 min]{.duree}

Présentées par le formateur à partir du document **Consignes de la Note 1**, déposé sur Moodle : déroulé, livrables, critères, Journal du Familier, rendu.

## 8. Note 1 [1 h 15]{.duree}

En individuel. Le sujet est distribué à 10h30.

## 9. Préparation de la Note 2 [15 min]{.duree}

Constitution des trinômes, puis tirage au sort d'un Sujet de Note 2 par groupe : un jeu différent de Félicia. C'est une **simple prise de connaissance** : aucun travail n'est attendu avant la Séance 3, où 30 minutes sont prévues pour lancer la Note 2.

::: bloc
### À retenir de la Séance 2

- Le MLD se **déduit** du MCD par des règles ; un outil les applique, mais ne connaît pas vos règles de gestion : relisez toujours ce qu'il génère.
- L'héritage a **trois** traductions : une seule table, une table par entité, les filles seulement. Choisir, c'est arbitrer entre colonnes vides, jointures et garanties.
- 1FN : pas de liste dans une colonne. 2FN : tout dépend de toute la clé. 3FN : rien ne dépend d'une colonne non clé.
- Dénormaliser, c'est **recopier** une information pour la lire plus vite. On le décide pour une charge précise, on le mesure, et on prévoit qui maintient la copie.
:::

En fin de Séance, **arrêtez votre Codespace** (fin du guide) : vous le rouvrirez en Séance 3.
