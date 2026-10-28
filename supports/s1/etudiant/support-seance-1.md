---
title: Du cahier des charges au MCD
soustitre: Modéliser le monde de Félicia avec les notions avancées de Merise
surtitre: Séance 1 · Lundi 9 novembre, 13h00 à 16h00
public: Support étudiant
---

## Le programme de la Séance

| Heure | Bloc | Durée |
|---------------|------------------------------------------------------|---------|
| 13h00 | Lancement : le module, le Fil rouge, les Notes, le Familier, l'outil | 20 min |
| 13h20 | Bug Hunt n°1 | 15 min |
| 13h35 | Apport théorique interactif : Merise avancé sur Félicia | 30 min |
| 14h05 | Pause | 10 min |
| 14h15 | Atelier en binôme : le MCD de Félicia, et deux Tickets du Game Designer | 50 min |
| 15h05 | Le Familier a dessiné un MCD | 25 min |
| 15h30 | Boss de fin de Séance | 20 min |
| 15h50 | Bilan et annonce de la Séance 2 | 10 min |

Vous avez reçu en début de Séance le **cahier des charges de Félicia**. Gardez-le sous la main : il sert à l'atelier, au Familier et au Boss.

## 1. Lancement [20 min]{.duree}

### Le module en une phrase

Choisir, concevoir et **justifier** la couche de données d'une application avant d'écrire une ligne de code : Merise avancé (Séances 1 et 2), les paradigmes NoSQL (Séance 3), puis une architecture polyglotte qui combine SQL et NoSQL (Séance 4).

### Le Fil rouge : *Neuf Vies : Les Îles de Félicia*

Toutes les démonstrations et tous les ateliers portent sur un même jeu, édité par le studio **Griffe & Grimoire** : un action-RPG en ligne dans un archipel d'îles flottantes peuplé de chats-mages.

- Un **Joueur** (la personne humaine) incarne un ou plusieurs **Héros** (des chats-mages).
- Chaque Héros appartient à une **Lignée** (Sorcier, Rôdeur d'ombre, Gardien, Alchimiste), peut rejoindre un **Clan**, collectionne des **Trésors** et dépense des **Pelotes d'or**.
- Mécanique signature : **9 Vies par Saison et par Héros**. Perdre une Vie est un événement tracé.

Le même univers servira à tout : Joueurs et boutique en relationnel, Trésors en document, classements en clé-valeur, télémétrie des Vies en colonne, réseau des Clans en graphe.

### Les deux Notes

::: bloc
| | Note 1 | Note 2 |
|----------------|-------------------------------------------|-------------------------------------------|
| Quand | fin de Séance 2, 1 h 15 | Séance 4 |
| Format | individuelle | en trinôme |
| Sujet | une fonctionnalité d'**un autre jeu** que Félicia | un autre jeu, tiré au sort en fin de Séance 2 |
| Production | MCD et MLD dans Looping, justification d'un choix de dénormalisation, Journal du Familier | architecture polyglotte, puis adaptation au **Patch Day** et ADR, Journal du Familier |
| Poids | **40 %** | **60 %** |

Tout se fait **pendant les Séances** : aucun travail n'est demandé entre deux Séances, ni avant une Note.
:::

Les ateliers, le Bug Hunt et le Boss sont de l'**Évaluation formative** : ils ne comptent pas dans la moyenne, ils servent à vous situer avant les Notes.

### Le Familier

Dans ce module, l'IA générative s'appelle le **Familier** : un compagnon utile, qui affirme parfois des choses fausses avec un aplomb parfait.

- Il est **autorisé partout**, y compris pendant la Note 1 et la Note 2.
- Ce qui est évalué, c'est votre **jugement de conception** et sa justification, pas la production d'un schéma.
- Chaque Note comprend un **Journal du Familier** : vos prompts copiés tels quels et, pour chacun, « gardé, rejeté ou modifié, parce que... ». Il compte pour 15 % de la Note 1 et 20 % de la Note 2. Le mode d'emploi est sur Moodle.
- Trois temps du module vous apprennent à vous en servir : aujourd'hui, **« Le Familier a dessiné un MCD »** ; en Séance 3, **« Demande au Familier »** ; en Séance 4, le **Patch Day**.

### L'outil : Looping, ou Mocodo en ligne [5 min]{.duree}

Suivez le guide **« Installer Looping ou ouvrir Mocodo »** : Looping sous Windows, Mocodo en ligne sur Mac ou Linux. Pas prêt au bout de 5 minutes ? Passez à Mocodo en ligne et prévenez le formateur.

Créez tout de suite dans Looping un fichier `felicia.loo` (sous Mocodo : un fichier texte `felicia.mcd`). C'est **lui** qui recevra les fragments de l'apport théorique, puis votre MCD de l'atelier.

## 2. Bug Hunt n°1 [15 min]{.duree}

Un stagiaire du studio a dessiné le MCD de Félicia en dix minutes, sans lire le cahier des charges jusqu'au bout. Le voici.

![Le MCD du stagiaire : six erreurs s'y cachent](bug-hunt-1.svg)

::: bloc
### En binôme, 8 minutes

1. Lisez le schéma **à voix haute**, association par association, dans les deux sens : « un Joueur adhère à... ; un Clan... ».
2. Comparez chaque phrase au cahier des charges.
3. Notez chaque erreur en une ligne : **où** elle est, **pourquoi** c'est faux.

Il y a **six erreurs**. Pas besoin de ressaisir le schéma : annotez-le sur le support ou sur une feuille.
:::

Le texte Mocodo du schéma (sans les types de données), pour le manipuler dans Mocodo en ligne si vous le souhaitez :

```text
JOUEUR: id_joueur, pseudo, courriel, nom_heros, lignée, vies_restantes
ADHÉRER, 0N JOUEUR, 11 CLAN: date_adhesion
CLAN: id_clan, nom_clan, devise

OBTENIR, 0N JOUEUR, 11 TRÉSOR, 0N ÎLE: date_obtention
:
ABRITER, 0N CLAN, 11 ÎLE

TRÉSOR: id_tresor, nom_tresor, nature, rareté
:
ÎLE: id_ile, nom_ile
```

Correction collective ensuite : vos erreurs relevées serviront de point de départ à l'apport théorique.

## 3. Apport théorique interactif [30 min]{.duree}

Trois fragments vont être saisis **pendant l'apport**, dans votre fichier `felicia` : vous les reprendrez **tels quels** dans l'atelier. Le formateur vous laisse le temps de chaque saisie. Sous Mocodo, copiez le texte donné sous chaque fragment.

### Rappel actif : ce que le Bug Hunt nous a appris

À partir de vos erreurs, on reconstruit ensemble :

- **Entité** : un concept du métier qui a une existence propre et un **identifiant** (souligné).
- **Association** : un lien entre entités, nommé par un verbe ; elle peut porter des attributs (la date d'adhésion).
- **Cardinalités** : sur chaque patte, le nombre minimum et maximum de participations **d'une occurrence de l'entité** à l'association : 0,1 ; 1,1 ; 0,N ; 1,N. On les lit depuis l'entité : « un Clan abrite... » se lit sur la patte du Clan.
- **Deux concepts proches ne sont pas un seul concept** : un Joueur et un Héros n'ont ni le même identifiant, ni la même durée de vie, ni les mêmes attributs. Les fusionner interdit d'avoir plusieurs Héros.

### L'héritage : les Lignées

Tous les Héros partagent un nom, un niveau, une date de création. Mais chaque Lignée apporte **une caractéristique que les autres n'ont pas** : l'élément d'un Sorcier, la furtivité d'un Rôdeur d'ombre, le rempart d'un Gardien, les recettes d'un Alchimiste.

Mettre ces quatre attributs dans HÉROS laisserait un Sorcier avoir une furtivité. L'**héritage** (ou spécialisation) range chaque attribut propre dans une **entité fille**, qui hérite de l'identifiant et des attributs de l'entité mère.

![Fragment 1 : le Joueur, ses Héros et les quatre Lignées](apport-lignees.svg)

Le triangle porte les contraintes de l'héritage :

- **X** (exclusion) : un Héros appartient à **au plus une** Lignée ;
- **T** (totalité) : un Héros appartient à **au moins une** Lignée ;
- **XT** (partition) : les deux à la fois, une et une seule Lignée. C'est le cas de Félicia : « ce choix est définitif ».

```text
SORCIER: élément
RÔDEUR_D_OMBRE: furtivité
JOUEUR: id_joueur, pseudo

GARDIEN: rempart
/XT\ HÉROS <= SORCIER, RÔDEUR_D_OMBRE, GARDIEN, ALCHIMISTE
INCARNER, 1N JOUEUR, 11 HÉROS

ALCHIMISTE: recettes_connues
:
HÉROS: id_heros, nom_heros, niveau
```

::: encadre
**Saisie, 3 minutes.** Le Joueur, le Héros, l'association INCARNER, puis l'héritage et ses quatre entités filles (geste décrit dans le mémo du guide Looping). Les autres attributs du Joueur et du Héros s'ajoutent pendant l'atelier.
:::

### L'association réflexive : le mentorat

Un Héros de niveau 30 au moins peut devenir le **mentor** de Héros débutants. Les deux pattes de l'association vont vers la **même entité** : c'est une association réflexive. Pour savoir qui est qui, chaque patte porte un **rôle**.

![Fragment 2 : le mentorat, une association réflexive](apport-mentorat.svg)

- Côté **apprenti** : 0,1. Un apprenti n'a qu'un seul mentor à la fois, et un Héros n'est pas forcément apprenti.
- Côté **mentor** : 0,N. Un mentor suit quelques apprentis, ou aucun.

Sous Mocodo, ajoutez à la fin de votre texte la seule ligne nouvelle (HÉROS y est déjà) :

```text
MENTORER, 0N [mentor] HÉROS, 01 [apprenti] HÉROS
```

::: encadre
**Saisie, 1 minute.** Une association, deux liens vers HÉROS, un rôle sur chaque lien.
:::

### L'association ternaire : un Héros obtient un Trésor sur une Île

Le studio veut savoir « quel Héros a obtenu quel Trésor, sur quelle Île et à quel moment ». Les trois entités participent **ensemble** au même fait : c'est une association **ternaire**, qui porte la date.

![Fragment 3 : l'obtention d'un Trésor, une association ternaire](apport-obtention.svg)

Un Trésor est un **exemplaire** : il n'est obtenu qu'**une seule fois**. Sa patte est donc 1,1. Cela veut dire qu'un Trésor suffit à retrouver le Héros et l'Île de son obtention : on y revient dans les contraintes. Deux associations binaires (Trésor–Héros et Trésor–Île, en 1,1 côté Trésor) seraient donc justes aussi ; la ternaire dit mieux qu'il s'agit d'un seul fait. Si un même Trésor pouvait être obtenu plusieurs fois, par des Héros et sur des Îles différents, les deux binaires ne diraient plus qui l'a obtenu où : la ternaire redeviendrait nécessaire.

Sous Mocodo, ajoutez les trois lignes nouvelles, sur une nouvelle rangée (la ligne vide). L'Île est celle des éléments fournis du cahier des charges : quand vous collerez ces éléments pendant l'atelier, **sautez leur première ligne** (`ÎLE: ...`), sinon Mocodo refuse le texte (« Duplicate entity »).

```text

OBTENIR, 0N HÉROS, 11 TRÉSOR, 0N ÎLE: date_obtention
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
TRÉSOR: id_tresor, nom_tresor, nature, rareté
```

::: encadre
**Saisie, 2 minutes.** Le Trésor, l'Île (celle des éléments fournis du cahier des charges, avec son identifiant et son nom), et l'association à trois liens.
:::

### Les contraintes

Un MCD peut dire plus que des cardinalités. Quand vous ne savez pas dessiner une contrainte, écrivez-la en règle de gestion : c'est juste aussi.

| Contrainte | Ce qu'elle dit | Sur Félicia |
|-----------------------------|----------------------------------------------|-------------------------------------------|
| **Partition (XT)** | chaque occurrence de la mère est dans une et une seule fille | un Héros a une et une seule Lignée |
| **Intégrité fonctionnelle (CIF)** | dans une association, certaines entités en déterminent une autre | un Trésor détermine le Héros et l'Île de son obtention (patte 1,1 de la ternaire) |
| **Inclusion (I)** | les occurrences d'une association sont incluses dans celles d'une autre | le chef d'un Clan fait partie des membres de ce Clan |
| **Exclusion (X)** | une même occurrence ne peut pas participer aux deux associations | une Vie perdue n'est pas prise par le Héros qui l'a perdue (PERDRE et PRENDRE, en duel) |

### Les règles de gestion, dont les 9 Vies

Une **règle de gestion** est une phrase du métier, écrite sans ambiguïté, que le modèle doit respecter. Certaines se voient dans le MCD (« un Héros appartient à un seul Joueur » : la cardinalité 1,1). D'autres **ne s'y voient pas** et s'écrivent à côté du schéma :

- « un Clan ne dépasse jamais cinquante Héros » : un MCD ne dessine pas de maximum chiffré ;
- « un mentor a un niveau d'au moins 30 et n'appartient pas au même Joueur que son apprenti » ;
- « chaque Héros dispose de 9 Vies par Saison ».

À vous : formulez ensemble la règle des 9 Vies. Que faut-il garder en mémoire pour l'appliquer ? Un compteur, ou chaque Vie perdue ? Rattachée à quoi ?

## 4. Pause [10 min]{.duree}

## 5. Atelier en binôme : le MCD de Félicia [50 min]{.duree}

::: bloc
### Ce que vous produisez

À partir du **cahier des charges**, dans votre fichier `felicia` qui contient déjà les trois fragments de l'apport :

1. le **MCD** de Félicia, limité à six concepts : **Joueur, Héros, Lignée, Clan, Trésor et Vies** ;
2. à côté du MCD, les **règles de gestion** qu'il ne montre pas, dont celle des 9 Vies ;
3. au moins **trois ambiguïtés** repérées, avec l'hypothèse retenue pour chacune, en une ligne.

Deux **Tickets du Game Designer** tomberont pendant l'atelier : le formateur les annonce, vous les traitez dès leur arrivée.
:::

| Repère | Ce que vous faites |
|---------------|------------------------------------------------------------------------|
| 14h15 | Lecture du cahier des charges à deux, crayon en main : règles et ambiguïtés au passage |
| vers 14h22 | Les éléments fournis complétés (zone, Saison : l'Île est déjà là), les attributs du Joueur et du Héros, le propriétaire actuel de chaque Trésor |
| 14h30 | **Ticket du Game Designer n°1** |
| 14h40 | **Ticket du Game Designer n°2** |
| ensuite | Les Clans (appartenance datée, repaire), puis les Vies perdues |
| si le temps le permet | Le chef du Clan, les alliances |
| 15h02 | Enregistrement : gardez votre MCD ouvert pour le bloc suivant |

Partagez-vous le travail : l'un tient la souris, l'autre écrit les règles de gestion et les hypothèses au fil de l'eau. Échangez à chaque Ticket.

## 6. Le Familier a dessiné un MCD [25 min]{.duree}

Pour préparer ce support, le formateur a fait ce qu'un étudiant pressé ferait : il a demandé au Familier de faire le MCD, avec un prompt écrit en dix secondes, suivi du cahier des charges complet copié-collé.

::: encadre
### Le prompt, tel qu'il a été envoyé

```text
fais moi le MCD de ce cahier des charges stp, en syntaxe mocodo

[suivi du texte intégral du cahier des charges de Félicia]
```
:::

La réponse du Familier est reproduite **telle quelle** ci-dessous. Elle n'a pas été retouchée.

<!-- lint-vocabulaire: ignorer-debut (réponse du Familier citée telle quelle) -->

::: encadre
Voici un MCD Mocodo limité aux six concepts demandés. Les entités **ÎLE**, **ZONE** et **SAISON** reprennent les éléments fournis.

```text
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
COMPRENDRE, 1N ÎLE, _11 ZONE
ZONE: nom_zone [VARCHAR(40)]
SAISON: id_saison [INTEGER], nom_saison [VARCHAR(40)]

JOUEUR: id_joueur, pseudo, email, pays, date_inscription
CRÉER, 0N JOUEUR, 11 HÉROS
HÉROS: id_heros, nom_heros, niveau, date_creation, element_maitrise, furtivite, solidite_rempart, nb_recettes
CHOISIR, 0N LIGNÉE, 11 HÉROS
LIGNÉE: id_lignee, nom_lignee

APPARTENIR, 0N CLAN, 01 HÉROS, date_entree
CLAN: id_clan, nom_clan, devise, date_fondation
REPAIRE, 0N ÎLE, 11 CLAN

MENTORER, 0N HÉROS [mentor], 01 HÉROS [apprenti]

TRÉSOR: id_tresor, nom_tresor, nature, rarete
POSSÉDER, 0N HÉROS, 01 TRÉSOR
OBTENIR, 0N HÉROS, 0N TRÉSOR, 0N ÎLE, date_obtention

VIE: id_vie, numero_vie_perdue, moment_perte, cause
PERDRE, 0N HÉROS, 11 VIE
PENDANT, 0N SAISON, 11 VIE
SURVENIR, 0N ZONE, 11 VIE
PRENDRE, 0N HÉROS, 01 VIE
```

**Règles de gestion à écrire à côté du MCD**

- `pseudo`, `nom_heros` et `nom_clan` sont uniques sur le serveur. Un Héros a exactement une Lignée, choisie définitivement.
- Selon sa Lignée, **une seule** des quatre caractéristiques spécifiques du Héros est renseignée : élément maîtrisé, furtivité, solidité du rempart ou nombre de recettes. Le niveau va de 1 à 60 ; furtivité et solidité vont de 1 à 100.
- Un Clan compte au plus 50 membres. Son chef doit être l'un de ses membres. Un mentor est de niveau 30 au moins, ne peut être son propre apprenti et ne peut pas avoir le même Joueur que son apprenti.
- Pour un couple **Héros–Saison**, il existe au plus neuf Vies perdues. Leurs numéros sont uniques et vont de 1 à 9, dans l'ordre des pertes. Les Vies restantes valent `9 − nombre de pertes` pour la Saison. `PRENDRE` désigne un autre Héros uniquement lorsque la cause est « duel ».
- La zone d'une Vie perdue détermine son Île. Le moment de la perte doit se situer pendant la Saison concernée.
- Un Trésor légendaire représente un exemplaire unique et a au plus un possesseur actuel. Lors d'un échange, son possesseur actuel change, tandis que son historique d'obtention est conservé.

**Ambiguïtés et hypothèses retenues**

1. **Trésors ordinaires** : une ligne `TRÉSOR` représente un exemplaire physique ; plusieurs exemplaires peuvent donc avoir le même nom.
2. **Obtention et échange** : `OBTENIR` couvre aussi la réception d'un échange ; l'Île enregistrée est celle où le Héros reçoit le Trésor.
3. **Clan quitté** : on conserve seulement le Clan actuel et sa date d'entrée, pas l'historique des anciens Clans.
4. **Mentorat** : on conserve seulement le mentor actuel, sans historique des mentorats.

**Limite du MCD de séance 1 :** une association Mocodo `OBTENIR` ne distingue pas proprement deux obtentions successives du *même exemplaire* par le même Héros sur la même Île. Pour garantir un historique complet des échanges légendaires, il faudra faire d'**OBTENTION** une entité événement dotée de son propre identifiant lors de l'extension du modèle.
:::

<!-- lint-vocabulaire: ignorer-fin -->

Collé tel quel dans Mocodo, ce texte est **refusé** : trois lignes ne respectent pas la syntaxe. Une fois ces trois lignes réparées (et rien d'autre), voici le schéma obtenu.

![Le MCD du Familier, après réparation de ses trois fautes de syntaxe](familier-mcd-s1.svg)

::: bloc
### En binôme, 12 minutes

Comparez le MCD du Familier **au vôtre**, et à son propre texte. Remplissez le tableau ci-dessous. Pour chaque erreur : où elle est, pourquoi c'est faux, d'après quelle phrase du cahier des charges. Visez trois erreurs, pas toutes : la mise en commun complète.
:::

<div class="remplir haut">

| Ce que le Familier fait bien | Ce que le Familier fait mal | Où il se contredit lui-même |
|---------------------------------|------------------------------------|------------------------------------|
| | | |
| | | |
| | | |

</div>

### Synthèse : où le Familier aide, où il échoue, comment mieux le solliciter

On complète ensemble, après la mise en commun.

<div class="remplir haut">

| Le Familier est utile pour... | Le Familier échoue sur... | Pour mieux le solliciter... |
|---------------------------------|-------------------------------------|-------------------------------------|
| | | |
| | | |
| | | |

</div>

## 7. Boss de fin de Séance [20 min]{.duree}

L'énoncé est distribué au début du bloc. Seul, en temps limité, puis correction collective.

## 8. Bilan [10 min]{.duree}

::: bloc
### À retenir de la Séance 1

- Un MCD se **lit** à voix haute, dans les deux sens de chaque association : c'est le meilleur détecteur d'erreurs.
- Deux concepts proches (Joueur et Héros) ne se fusionnent pas : identifiant, durée de vie et attributs les distinguent.
- **Héritage** quand des sous-types ont des attributs propres ; **réflexive** quand une entité se lie à elle-même, avec des rôles ; **ternaire** quand trois entités participent ensemble au même fait.
- Les **contraintes** (XT, CIF, inclusion, exclusion) et les **règles de gestion** disent ce que les cardinalités ne disent pas.
- Le Familier produit vite un premier jet plausible. Votre travail : vérifier chaque cardinalité et chaque règle implicite contre le cahier des charges.
:::

### Séance 2 : mardi 10 novembre, 8h00 à 12h00

Du MCD au MPD : on traduit le MCD de Félicia en tables, on normalise, puis on dénormalise à bon escient en mesurant le gain dans PostgreSQL. Votre environnement (un Codespace) se met en place **pendant la Séance**, en 20 minutes, sans rien installer avant. La Séance se termine par la **Note 1** (1 h 15) et par le tirage au sort des Sujets de Note 2.

Rien à préparer d'ici là. Si vous voulez, gardez votre fichier `felicia` : il vous servira de point de comparaison.
