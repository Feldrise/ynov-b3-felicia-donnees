---
title: Installer Looping ou ouvrir Mocodo
soustitre: L'outil de modélisation du module, prêt en 5 minutes
surtitre: Séance 1 · Lancement
public: Support étudiant
---

## Quel outil pour toi ?

Les ateliers et les Notes se font dans **Looping**, un logiciel gratuit de l'Université de Toulouse, fidèle à Merise, qui génère aussi le MLD et le script SQL. Il ne tourne que sous Windows : sur Mac ou Linux, tu prends **Mocodo en ligne**, qui dessine les mêmes diagrammes à partir d'un texte.

::: bloc
### Pendant le Lancement : l'installation seulement

Windows, partie 1 ; Mac ou Linux, partie 2 ; 5 minutes au plus. Si ça bloque, ou si ce n'est pas prêt au bout des 5 minutes, passe sur Mocodo en ligne, qui marche partout, et fais-moi signe. Le reste du guide est un mémo pour plus tard.
:::

## 1. Looping sous Windows [5 min]{.duree}

Looping est un **exécutable portable** : ni installation, ni droits d'administrateur.

1. Sur **www.looping-mcd.fr**, clique sur **Télécharger** : tu obtiens `Looping.zip` (environ 7 Mo), qui contient une version 64 bits et une version 32 bits.
2. Clic droit sur `Looping.zip`, **Extraire tout**, dans un dossier à toi (par exemple `Documents\Looping`). Ne lance pas Looping depuis l'intérieur de l'archive.
3. Double-clique sur `Looping.exe` (la version 64 bits).
4. Si Windows affiche « Windows a protégé votre ordinateur », clique sur **Informations complémentaires**, puis **Exécuter quand même** : le logiciel n'est simplement pas signé.

C'est prêt quand Looping s'ouvre sur une feuille vide.

::: {.encadre .attention}
L'antivirus bloque Looping ? Ne perds pas de temps : Mocodo en ligne pour cette Séance, et préviens-moi.
:::

## 2. Mocodo en ligne sous Mac ou Linux [2 min]{.duree}

1. Ouvre **www.mocodo.net** dans ton navigateur.
2. Lance la génération sur l'exemple déjà affiché.

C'est prêt quand le diagramme de l'exemple apparaît à côté du texte.

## Mémo : se servir de l'outil

Reviens-y quand tu en as besoin.

### Les gestes de base dans Looping

- **Entité** : outil entité, clic sur la feuille, double-clic pour la nommer et ajouter ses attributs. Indique l'**identifiant**, que Looping souligne.
- **Association** : outil association, entre deux entités ; nomme-la d'un verbe et relie-la à chacune.
- **Cardinalités** : minimum et maximum sur chaque lien (0,1 ; 1,1 ; 0,N ; 1,N).
- **Identification relative** : dans les propriétés du lien entre l'entité dépendante et son association, coche l'identifiant relatif ; Looping écrit alors (1,1).
- **Héritage** : outil héritage sous l'entité mère, relié à la mère et à chaque entité fille.
- **MLD et script SQL** : générés depuis le MCD. Relis-les toujours : généré ne veut pas dire juste.
- **Enregistrer** : dans un fichier `.loo`, celui que tu rendras avec tes Notes.

### Mocodo en ligne : écrire et garder son MCD

Efface l'exemple, saisis ton MCD et lance la génération ; Mocodo donne aussi le MLD et le script SQL. Pour garder ton travail, copie le texte dans un fichier `.mcd` et télécharge l'image : ce `.mcd` remplace le `.loo` pour rendre une Note. Pense à copier ton texte avant de fermer l'onglet.

### La syntaxe Mocodo en six règles

```text
CLAN: id_clan, nom_clan, devise
ABRITER, 11 CLAN, 0N ÎLE
ÎLE: id_ile, nom_ile
```

1. **Une entité** : son nom, deux-points, ses attributs séparés par des virgules. Le **premier attribut est l'identifiant**.
2. **Une association** : son nom, puis chaque entité reliée, précédée de sa cardinalité : `11`, `01`, `0N` ou `1N` (1,1 ; 0,1 ; 0,N ; 1,N dans Looping).
3. **Un attribut porté par l'association** : après deux-points, en fin de ligne (`ASSOCIATION, 0N ENTITÉ_A, 0N ENTITÉ_B: attribut`).
4. **Une association réflexive** : la même entité deux fois, un rôle entre crochets sur chaque patte (`ASSOCIATION, 0N [rôle 1] ENTITÉ, 01 [rôle 2] ENTITÉ`). Une ternaire relie trois entités sur la même ligne.
5. **Un héritage** : le triangle, l'entité mère, puis les entités filles (`/XT\ HÉROS <= SORCIER, GARDIEN`). XT : chaque Héros appartient à une et une seule entité fille.
6. **La disposition** : une ligne vide commence une nouvelle rangée du diagramme.

### Un exemple complet : le repaire d'un Clan

**Chaque Clan a son repaire sur une Île ; une Île peut abriter le repaire de plusieurs Clans, ou d'aucun.**

![Le repaire d'un Clan, dessiné par Mocodo](exemple-repaire.svg)

Le texte Mocodo, avec les types de données qui serviront au script SQL :

```text
CLAN: id_clan [INTEGER], nom_clan [VARCHAR(60)], devise [VARCHAR(160)]
ABRITER, 11 CLAN, 0N ÎLE
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
```

Le MLD généré :

- **CLAN** (<u>id_clan</u>, nom_clan, devise, *#id_ile*)
- **ÎLE** (<u>id_ile</u>, nom_ile)

::: encadre
#### Pourquoi la clé étrangère va dans CLAN

Un Clan a exactement un repaire (1,1) : ABRITER disparaît au MLD et l'identifiant de l'Île migre dans CLAN. On y revient en Séance 2.
:::

## Comment tu recevras les schémas du module

Les schémas distribués (le MCD piégé du Bug Hunt, le MCD dessiné par le Familier) sont **projetés** et donnés dans le support avec leur texte Mocodo. On les lit et on les annote, **sans les ressaisir** : tu ne saisis que **ton propre MCD**, celui de l'atelier ou de la Note. Tu peux toujours coller leur texte dans Mocodo en ligne pour les manipuler.
