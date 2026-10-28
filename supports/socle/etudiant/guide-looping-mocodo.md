---
title: Installer Looping ou ouvrir Mocodo
soustitre: L'outil de modélisation du module, prêt en 5 minutes
surtitre: Séance 1 · Lancement
public: Support étudiant
---

## Quel outil pour vous ?

Dans ce module, les MCD et les MLD se dessinent dans **Looping** : un logiciel gratuit de l'Université de Toulouse, fidèle à Merise, qui génère aussi le MLD et le script SQL. C'est l'outil des ateliers et des Notes, et il permet une correction homogène.

Looping ne fonctionne que sous Windows. Sur Mac ou Linux, vous utilisez **Mocodo en ligne**, qui produit les mêmes diagrammes à partir d'un texte.

::: bloc
### Pendant le Lancement : l'installation seulement

- **Windows** : Looping, partie 1.
- **Mac ou Linux** : Mocodo en ligne, partie 2.

Une seule des deux parties vous concerne. Comptez 5 minutes au plus. Bloqué sur une étape, ou pas encore prêt au bout de ces 5 minutes ? Passez à Mocodo en ligne, qui fonctionne sur tous les postes, et prévenez le formateur.

La suite du guide (les gestes de base, la syntaxe Mocodo, un exemple) est un mémo à consulter pendant l'atelier ou les Notes : rien à en faire pendant le Lancement.
:::

## 1. Looping sous Windows [5 min]{.duree}

Looping est un **exécutable portable** : il se lance sans installation et sans droits d'administrateur.

1. Ouvrez **www.looping-mcd.fr** et cliquez sur **Télécharger** : vous obtenez une archive `Looping.zip` (environ 7 Mo) qui contient une version 64 bits et une version 32 bits.
2. Dans l'explorateur de fichiers, faites un clic droit sur `Looping.zip`, choisissez **Extraire tout**, et extrayez l'archive dans un dossier à vous (par exemple `Documents\Looping`). Ne lancez pas Looping depuis l'intérieur de l'archive.
3. Double-cliquez sur `Looping.exe` (la version 64 bits).
4. Si Windows affiche « Windows a protégé votre ordinateur », cliquez sur **Informations complémentaires**, puis sur **Exécuter quand même**. Le logiciel n'est simplement pas signé.

C'est prêt quand Looping s'ouvre sur une feuille vide.

::: {.encadre .attention}
Si l'antivirus de votre poste bloque Looping, ne perdez pas de temps : utilisez Mocodo en ligne pour cette Séance et signalez-le au formateur.
:::

## 2. Mocodo en ligne sous Mac ou Linux [2 min]{.duree}

Mocodo dessine un MCD à partir d'un texte : une ligne par entité, une ligne par association.

1. Ouvrez **www.mocodo.net** dans votre navigateur. Rien à installer.
2. Lancez la génération sur l'exemple déjà affiché dans la zone de texte.

C'est prêt quand le diagramme de l'exemple apparaît à côté du texte.

## Mémo : se servir de l'outil

Cette partie n'a pas de créneau : revenez-y quand vous en avez besoin.

### Les gestes de base dans Looping

- **Créer une entité** : choisissez l'outil entité dans la barre d'outils, cliquez sur la feuille, puis double-cliquez sur l'entité pour la nommer et lui ajouter ses attributs. Indiquez quel attribut est l'**identifiant** : Looping le souligne.
- **Créer une association** : choisissez l'outil association, posez-la entre deux entités, nommez-la avec un verbe, puis reliez-la à chaque entité.
- **Saisir les cardinalités** : sur chaque lien, choisissez le minimum et le maximum (0,1 ; 1,1 ; 0,N ; 1,N).
- **Identification relative** : dans les propriétés du lien entre l'entité qui dépend d'une autre et son association, cochez l'identifiant relatif ; Looping écrit alors la cardinalité entre parenthèses, (1,1).
- **Créer un héritage** : choisissez l'outil héritage, posez le symbole sous l'entité mère, puis reliez-le à la mère et à chacune des entités filles.
- **Voir le MLD et le script SQL** : Looping les génère à partir du MCD. Relisez-les toujours : un MLD généré n'est pas forcément un MLD juste.
- **Enregistrer** : Looping enregistre votre travail dans un fichier `.loo`. C'est ce fichier que vous rendrez avec vos Notes.

### Mocodo en ligne : écrire et garder son MCD

- Effacez l'exemple affiché dans la zone de texte et saisissez votre MCD, puis lancez la génération. Mocodo peut aussi afficher le MLD et produire le script SQL.
- Pour garder votre travail, copiez le texte dans un fichier `.mcd` sur votre ordinateur, et téléchargez l'image du diagramme. C'est le texte `.mcd` qui remplace le fichier `.loo` de Looping au moment de rendre une Note.

### La syntaxe Mocodo en six règles

```text
CLAN: id_clan, nom_clan, devise
ABRITER, 11 CLAN, 0N ÎLE
ÎLE: id_ile, nom_ile
```

1. **Une entité** : son nom, deux-points, puis ses attributs séparés par des virgules. Le **premier attribut est l'identifiant**.
2. **Une association** : son nom, puis, pour chaque entité reliée, la cardinalité collée au nom de l'entité : `11`, `01`, `0N` ou `1N` (Looping écrit 1,1 ; 0,1 ; 0,N ; 1,N).
3. **Un attribut porté par l'association** : après deux-points, en fin de ligne (`ASSOCIATION, 0N ENTITÉ_A, 0N ENTITÉ_B: attribut`).
4. **Une association réflexive** : la même entité apparaît deux fois, avec un rôle entre crochets pour distinguer les deux pattes (`ASSOCIATION, 0N [rôle 1] ENTITÉ, 01 [rôle 2] ENTITÉ`). Une association ternaire relie simplement trois entités sur la même ligne.
5. **Un héritage** : un triangle, l'entité mère, puis les entités filles (`/XT\ HÉROS <= SORCIER, GARDIEN`). Les lettres XT signifient que chaque Héros appartient à une et une seule entité fille.
6. **La disposition** : une ligne vide commence une nouvelle rangée du diagramme.

### Un exemple complet : le repaire d'un Clan

**Chaque Clan a son repaire sur une Île ; une Île peut abriter le repaire de plusieurs Clans, ou d'aucun.**

![Le repaire d'un Clan, dessiné par Mocodo](exemple-repaire.svg)

Le texte Mocodo correspondant, avec les types de données qui serviront au script SQL :

```text
CLAN: id_clan [INTEGER], nom_clan [VARCHAR(60)], devise [VARCHAR(160)]
ABRITER, 11 CLAN, 0N ÎLE
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
```

Le MLD que l'outil génère :

- **CLAN** (<u>id_clan</u>, nom_clan, devise, *#id_ile*)
- **ÎLE** (<u>id_ile</u>, nom_ile)

::: encadre
#### Pourquoi la clé étrangère va dans CLAN

Un Clan a exactement un repaire (cardinalité 1,1) : l'association ABRITER disparaît au passage au MLD, et l'identifiant de l'Île migre dans la table CLAN. Vous reverrez cette règle de passage en Séance 2.
:::

## Comment vous recevrez les schémas du module

Les schémas distribués pendant le module (le MCD piégé du Bug Hunt, le MCD dessiné par le Familier) sont **projetés** et donnés dans le support PDF, avec leur texte Mocodo. On les lit, on les annote et on en discute : **vous n'avez pas à les ressaisir** dans Looping.

La seule saisie qui vous revient est celle de **votre propre MCD**, celui que vous construisez en atelier ou en Note. Sous Mac ou Linux, vous pouvez coller le texte Mocodo d'un schéma distribué dans Mocodo en ligne si vous voulez le manipuler, mais rien ne l'exige.
