---
title: Du cahier des charges au MCD
soustitre: Modéliser le monde de Félicia avec les notions avancées de Merise
surtitre: Séance 1 · Lundi 9 novembre, 13h00 à 16h00
public: Support étudiant
---

## Au programme

Lancement (20 min), Bug Hunt n°1 (15 min), apport sur Merise avancé (30 min), pause (10 min), atelier en binôme (50 min), « Le Familier a dessiné un MCD » (25 min), Boss (20 min), bilan (10 min).

Garde le **cahier des charges de Félicia** sous la main tout l'après-midi : il sert à l'atelier, au Familier et au Boss.

## 1. Lancement [20 min]{.duree}

### Ce qu'on va faire ensemble

Le but du module : choisir et concevoir la couche de données d'une application, et surtout **justifier** tes choix, avant d'écrire du code. Merise avancé en Séances 1 et 2, NoSQL en Séance 3, les deux ensemble en Séance 4.

### Le Fil rouge : *Neuf Vies : Les Îles de Félicia*

Tout le module tourne autour d'un même jeu, édité par le studio **Griffe & Grimoire** : un action-RPG en ligne, dans un archipel d'îles flottantes peuplé de chats-mages.

Un **Joueur**, la personne derrière l'écran, incarne un ou plusieurs **Héros**. Chaque Héros a sa **Lignée** (Sorcier, Rôdeur d'ombre, Gardien ou Alchimiste), peut rejoindre un **Clan**, collectionne des **Trésors** et dépense des **Pelotes d'or**. Et comme ce sont des chats, chaque Héros a **9 Vies par Saison**. Chaque Vie perdue est tracée.

### Les deux Notes

**Note 1** (40 %, seul, fin de Séance 2) : le MCD et le MLD d'un autre jeu que Félicia, plus un choix de dénormalisation à justifier, en 1 h 15. **Note 2** (60 %, en trinôme, Séance 4) : une architecture polyglotte pour un autre jeu tiré au sort, que tu adapteras au **Patch Day**.

Tout se fait en Séance, rien à préparer entre deux. Les ateliers, Bug Hunts et Boss sont de l'**Évaluation formative** : ils ne comptent pas, ils te disent où tu en es.

### Le Familier

Ici, l'IA générative s'appelle le **Familier**. C'est un compagnon utile, qui affirme parfois des choses fausses avec un aplomb parfait.

Tu peux t'en servir partout, Notes comprises : je note ton jugement, pas le schéma. Chaque Note comprend donc un **Journal du Familier** (tes prompts, et ce que tu en as gardé, rejeté ou modifié, et pourquoi), qui compte pour 15 % de la Note 1 et 20 % de la Note 2. On s'entraîne à trois moments : aujourd'hui, en Séance 3 avec « Demande au Familier », et en Séance 4 au Patch Day.

### L'outil [5 min]{.duree}

Suis le guide « Installer Looping ou ouvrir Mocodo » : Looping sous Windows, Mocodo en ligne sur Mac ou Linux. Si ça bloque au bout de 5 minutes, passe sur Mocodo en ligne et fais-moi signe.

Crée tout de suite un fichier `felicia.loo` (ou `felicia.mcd` sous Mocodo) : il recevra les fragments de l'apport, puis ton MCD.

## 2. Bug Hunt n°1 [15 min]{.duree}

Un stagiaire du studio a dessiné le MCD de Félicia en dix minutes, sans lire le cahier des charges jusqu'au bout. Il y a laissé **six erreurs**.

![Le MCD du stagiaire : six erreurs s'y cachent](bug-hunt-1.svg)

::: bloc
### En binôme, 8 minutes

Lisez le schéma à voix haute, association par association et dans les deux sens (« un Joueur adhère à… ; un Clan… »), puis comparez chaque phrase au cahier des charges. Notez chaque erreur en une ligne : où elle est, et pourquoi c'est faux. Pas besoin de ressaisir le schéma, annotez-le directement.
:::

Si tu veux le manipuler dans Mocodo en ligne, voici son texte :

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

On corrige ensemble juste après, et tes erreurs relevées lancent l'apport.

## 3. Apport théorique interactif [30 min]{.duree}

On saisit trois fragments pendant l'apport, dans ton fichier `felicia` : tu les reprendras tels quels à l'atelier. Sous Mocodo, copie le texte sous chaque fragment.

### Ce que le Bug Hunt nous a appris

Une **entité** a son propre identifiant ; une **association** relie des entités et peut porter des attributs ; les **cardinalités** se lisent depuis l'entité (« un Clan abrite… » se lit sur la patte du Clan).

Et Joueur et Héros sont deux concepts : identifiants, durées de vie et attributs différents. Fusionne-les, et plus personne n'a deux Héros.

### L'héritage : les Lignées

Chaque Lignée a sa caractéristique : l'élément du Sorcier, la furtivité du Rôdeur d'ombre, le rempart du Gardien, les recettes de l'Alchimiste. Tout mettre dans HÉROS, c'est permettre un Sorcier furtif. L'**héritage** range chaque attribut dans une entité fille.

![Fragment 1 : le Joueur, ses Héros et les quatre Lignées](apport-lignees.svg)

Le triangle dit combien de filles un Héros peut avoir : **X** pour au plus une, **T** pour au moins une, **XT** pour exactement une. Félicia est en XT : « ce choix est définitif ».

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
**Saisie, 3 minutes** : le Joueur, le Héros, INCARNER, puis l'héritage et ses quatre filles (le geste est dans le mémo du guide Looping). Les autres attributs viendront pendant l'atelier.
:::

### La réflexive : le mentorat

Un Héros de niveau 30 ou plus peut devenir mentor. Les deux pattes vont vers HÉROS : c'est une **réflexive**, avec un rôle sur chaque patte. Apprenti en 0,1 (un mentor au plus), mentor en 0,N.

![Fragment 2 : le mentorat, une association réflexive](apport-mentorat.svg)

Sous Mocodo, ajoute juste cette ligne (HÉROS est déjà là) :

```text
MENTORER, 0N [mentor] HÉROS, 01 [apprenti] HÉROS
```

::: encadre
**Saisie, 1 minute** : une association, deux liens vers HÉROS, un rôle sur chaque lien.
:::

### La ternaire : un Héros obtient un Trésor sur une Île

Le studio veut savoir quel Héros a obtenu quel Trésor, sur quelle Île, et quand. Les trois entités participent au même fait : c'est une association **ternaire**, qui porte la date.

![Fragment 3 : l'obtention d'un Trésor, une association ternaire](apport-obtention.svg)

Un Trésor n'est obtenu qu'une fois, d'où le 1,1. Il suffit donc à retrouver son Héros et son Île : deux binaires en 1,1 côté Trésor seraient justes aussi, la ternaire dit juste mieux qu'il s'agit d'un seul fait. Si un Trésor pouvait être obtenu plusieurs fois, par des Héros et sur des Îles différents, elle redeviendrait nécessaire.

Sous Mocodo, ajoute ces lignes sur une nouvelle rangée. À l'atelier, quand tu colleras les éléments fournis du cahier des charges, saute leur ligne `ÎLE: ...` : elle est déjà là, et Mocodo refuse les doublons (« Duplicate entity »).

```text

OBTENIR, 0N HÉROS, 11 TRÉSOR, 0N ÎLE: date_obtention
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
TRÉSOR: id_tresor, nom_tresor, nature, rareté
```

::: encadre
**Saisie, 2 minutes** : le Trésor, l'Île (avec son identifiant et son nom) et l'association à trois liens.
:::

### Les contraintes

Un MCD peut dire plus que des cardinalités :

- la **partition (XT)** : un Héros a une et une seule Lignée ;
- la **contrainte d'intégrité fonctionnelle (CIF)** : un Trésor détermine le Héros et l'Île de son obtention, c'est la patte 1,1 de la ternaire ;
- l'**inclusion (I)** : le chef d'un Clan fait partie de ses membres ;
- l'**exclusion (X)** : une Vie perdue en duel n'est pas prise par le Héros qui l'a perdue (PERDRE et PRENDRE).

Tu ne sais pas dessiner une contrainte ? Écris-la en règle de gestion, c'est juste aussi.

### Les règles de gestion, dont les 9 Vies

Une **règle de gestion** est une phrase du métier que le modèle doit respecter. Certaines se voient (« un Héros appartient à un seul Joueur », c'est le 1,1), d'autres s'écrivent à côté du schéma (« un Clan ne dépasse jamais cinquante Héros »).

À vous : formulez la règle des 9 Vies. Pour l'appliquer, que faut-il garder en mémoire ? Un compteur, ou chaque Vie perdue ? Et rattaché à quoi ?

## 4. Pause [10 min]{.duree}

## 5. Atelier en binôme : le MCD de Félicia [50 min]{.duree}

::: bloc
### Ce que vous rendez

Dans votre fichier `felicia`, qui contient déjà les trois fragments :

1. le **MCD** de Félicia, limité à six concepts : Joueur, Héros, Lignée, Clan, Trésor et Vies ;
2. à côté, les **règles de gestion** que le schéma ne montre pas, dont celle des 9 Vies ;
3. au moins **trois ambiguïtés** du cahier des charges, avec votre hypothèse pour chacune, en une ligne.

Deux **Tickets du Game Designer** vont tomber pendant l'atelier, vers 14h30 et 14h40. Traitez-les dès leur arrivée.
:::

Mon conseil : lisez le cahier des charges à deux, crayon en main. Complétez ensuite les éléments fournis (zone, Saison), les attributs du Joueur et du Héros, et le propriétaire actuel de chaque Trésor. Après les Tickets : les Clans (appartenance datée, repaire), puis les Vies perdues. Le chef et les alliances, seulement s'il reste du temps.

L'un tient la souris, l'autre écrit règles et hypothèses ; changez à chaque Ticket. Gardez le MCD ouvert à la fin, on s'en sert juste après.

## 6. Le Familier a dessiné un MCD [25 min]{.duree}

Pour préparer ce support, j'ai fait ce que ferait un étudiant pressé : j'ai demandé au Familier de faire le MCD, avec un prompt écrit en dix secondes et le cahier des charges collé en entier.

::: encadre
### Le prompt, tel quel

```text
fais moi le MCD de ce cahier des charges stp, en syntaxe mocodo

[suivi du texte intégral du cahier des charges de Félicia]
```
:::

Voici sa réponse, sans aucune retouche.

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

Ça a l'air sérieux, non ? Pourtant, collé tel quel dans Mocodo, ce texte est refusé : trois lignes ne respectent pas la syntaxe. Voici le schéma une fois ces trois lignes réparées, et rien d'autre.

![Le MCD du Familier, après réparation de ses trois fautes de syntaxe](familier-mcd-s1.svg)

::: bloc
### En binôme, 12 minutes

Comparez le MCD du Familier au vôtre, et à son propre texte. Pour chaque erreur : où elle est, pourquoi c'est faux, et quelle phrase du cahier des charges le montre. Visez trois erreurs, pas toutes : la mise en commun fera le reste.
:::

<div class="remplir haut">

| Ce que le Familier fait bien | Ce que le Familier fait mal | Où il se contredit lui-même |
|---------------------------------|------------------------------------|------------------------------------|
| | | |
| | | |
| | | |

</div>

### Ce qu'on en retient

On remplit ensemble après la mise en commun.

<div class="remplir haut">

| Le Familier est utile pour... | Le Familier échoue sur... | Pour mieux le solliciter... |
|---------------------------------|-------------------------------------|-------------------------------------|
| | | |
| | | |
| | | |

</div>

## 7. Boss de fin de Séance [20 min]{.duree}

Je distribue l'énoncé au début du bloc. Tu le fais seul, en temps limité, et on corrige ensemble.

## 8. Bilan [10 min]{.duree}

::: bloc
### À retenir

- Un MCD se lit à voix haute, dans les deux sens de chaque association. C'est le meilleur détecteur d'erreurs.
- Joueur et Héros se ressemblent, mais ce sont deux concepts : on ne les fusionne pas.
- Héritage pour des sous-types qui ont leurs propres attributs, réflexive quand une entité se lie à elle-même, ternaire quand trois entités font partie du même fait.
- Ce que les cardinalités ne disent pas passe par les contraintes ou les règles de gestion.
- Le Familier sort vite un premier jet plausible. À toi de vérifier chaque cardinalité et chaque règle implicite contre le cahier des charges.
:::

### Demain matin, Séance 2

Rendez-vous mardi 10 novembre, de 8h00 à 12h00. On traduira le MCD de Félicia en tables, on normalisera, puis on dénormalisera en mesurant le gain dans PostgreSQL. Ton environnement (un Codespace) se met en place pendant la Séance, en 20 minutes. La matinée se termine par la **Note 1**, puis par le tirage au sort des Sujets de Note 2.

Rien à préparer d'ici là. Garde juste ton fichier `felicia`, il te servira de point de comparaison. Un Héros a 9 Vies, ton MCD n'en a qu'une : sauvegarde-le.
