---
title: Cahier des charges de Félicia
soustitre: Ce que le studio Griffe & Grimoire attend de la base de données de Neuf Vies
surtitre: Fil rouge · Séance 1
public: Support étudiant
---

## Votre mission

Le studio **Griffe & Grimoire** prépare la prochaine version de *Neuf Vies : Les Îles de Félicia*, un action-RPG en ligne. Dans un archipel d'îles flottantes peuplé de chats-mages, des milliers de Joueurs incarnent des Héros qui explorent, combattent et collectionnent des Trésors.

Le studio vous recrute pour concevoir la base de données. Ce document est le cahier des charges rédigé par les game designers du studio : il décrit Félicia avec leurs mots, pas avec ceux d'un informaticien.

::: bloc
### Un cahier des charges volontairement réaliste

Comme dans un vrai projet, certaines règles sont **implicites** : elles ne sont pas écrites comme des règles, mais elles se déduisent du texte. Et certaines phrases sont **ambiguës** : deux lectures sont possibles, et le studio n'a pas tranché.

À vous d'extraire les règles de gestion, de repérer les ambiguïtés et d'**écrire l'hypothèse que vous retenez** pour chacune. Un modèle juste avec des hypothèses explicites vaut mieux qu'un modèle qui devine en silence.
:::

## L'archipel de Félicia

Félicia est un archipel de huit Îles flottantes, de l'Île de Velours, où tout Héros débute, à l'Île de Nuit-Sans-Fin, réservée aux plus aguerris. Chaque Île exige un **niveau minimum** : un Héros dont le niveau est inférieur ne peut pas y explorer.

Chaque Île est découpée en **zones** qui portent un nom : sur l'Île de Brume, par exemple, la Falaise des Soupirs, le Marais Sans Fond, le Pont des Lierres et le Phare Éteint. Le nom d'une zone n'est unique qu'à l'intérieur de son Île.

Le temps de Félicia est rythmé par les **Saisons**. Une Saison dure environ trois mois, porte un nom (la Saison en cours s'appelle la Saison de la Lune Rousse) et a une date de début et une date de fin.

::: encadre
Les Îles, leurs zones et les Saisons sont déjà modélisées : elles vous attendent en fin de document, parmi les éléments fournis pour l'atelier. Elles y sont réduites à leur identifiant et à leur nom : le niveau minimum d'une Île et les dates d'une Saison n'y figurent pas, et vous n'avez pas à les ajouter.
:::

## Les Joueurs et leurs Héros

Un **Joueur** est une personne réelle qui s'inscrit sur Neuf Vies. On connaît son pseudo, unique sur tout le serveur, son adresse électronique, son pays et sa date d'inscription.

Un Joueur incarne des **Héros** : des chats-mages qu'il crée et fait progresser. La plupart des Joueurs se contentent d'un seul Héros, mais beaucoup en ont deux, trois ou plus, pour essayer d'autres Lignées. Chaque Héros a un nom, unique sur le serveur, un niveau de 1 à 60 et une date de création.

> Extrait de la messagerie du studio : « Quand un Joueur se connecte, il choisit avec quel Héros il joue. Dans le classement, ce sont les Héros qui apparaissent, pas les Joueurs. »

## Les Lignées

À la création, le Joueur choisit la **Lignée** de son Héros. Ce choix est définitif. Il existe quatre Lignées, et chacune apporte une caractéristique que les autres n'ont pas :

| Lignée | Ce qui la distingue |
|-------------------------|---------------------------------------------------------------------------|
| Sorcier | l'élément qu'il maîtrise : feu, givre, foudre, lune ou lierre |
| Rôdeur d'ombre | sa furtivité, notée de 1 à 100 |
| Gardien | la solidité de son rempart, notée de 1 à 100 |
| Alchimiste | le nombre de recettes qu'il connaît |

Tous les Héros, quelle que soit leur Lignée, ont par ailleurs les mêmes informations : nom, niveau, date de création.

## Les Clans

Les Héros se regroupent en **Clans** pour jouer ensemble dans la durée. Un Clan a un nom unique, une devise, une date de fondation et un repaire, installé sur une Île. Un Héros qui quitte son Clan peut en rejoindre un autre ; le studio veut savoir depuis quand chaque Héros fait partie de son Clan. Un Clan ne dépasse jamais cinquante Héros.

Chaque Clan est dirigé par un **chef**, choisi parmi ses membres. Le chef et ses lieutenants décident des alliances.

Deux Clans peuvent en effet s'**allier**. Une alliance lie deux Clans à partir d'une date ; elle n'est pas orientée : « A est allié à B » équivaut à « B est allié à A ».

## Le mentorat

Un Héros expérimenté, de niveau 30 au moins, peut prendre sous son aile des Héros débutants : il devient leur **mentor**. Un apprenti n'a qu'un seul mentor à la fois. Un mentor suit quelques apprentis.

> Extrait de la messagerie du studio : « On a vu des Joueurs créer un deuxième Héros pour se servir de mentor à eux-mêmes. Il faut l'empêcher. »

## Les Trésors

En explorant, un Héros obtient des **Trésors** : armes, armures, grimoires, potions, reliques et parures. On veut savoir **quel Héros a obtenu quel Trésor, sur quelle Île et à quel moment**.

Chaque Trésor a un nom, une nature et une rareté : commun, rare, épique ou légendaire. Ses autres attributs dépendent de sa nature : une arme a des dégâts et une allonge, un grimoire contient une liste de sorts, une potion a un effet, une durée et un nombre de doses, une relique peut être maudite...

::: encadre
Les attributs propres à chaque nature de Trésor attendront la Séance 3 : dans le MCD de l'atelier de la Séance 1, un Trésor a seulement son identifiant, son nom, sa nature et sa rareté.
:::

Les Trésors **légendaires** sont uniques : il n'en existe qu'un exemplaire dans tout Félicia, et les Héros se les échangent.

> Extrait de la messagerie du studio : « La Griffe d'Aube est le Trésor le plus convoité du serveur. Trois Héros l'ont déjà eue entre les pattes. »
>
> « Les Dagues de Brume, on en trouve partout sur l'Île de Brume. Tout le monde en a une. »

## Les 9 Vies

C'est la mécanique qui fait l'identité de Neuf Vies : **chaque Héros dispose de 9 Vies par Saison**.

Quand un Héros perd une Vie, Neuf Vies enregistre l'événement : le moment exact, la zone où cela s'est produit et la cause (chute dans le vide, sortilège, gardien d'Île, piège, brume toxique ou duel). Lors d'un duel, la Vie est prise par un autre Héros, que l'on veut connaître. Au fil d'une Saison, les Vies perdues d'un Héros sont numérotées dans l'ordre : la première, la deuxième... jusqu'à la neuvième.

Un Héros qui a perdu ses 9 Vies s'endort jusqu'à la Saison suivante. Au début de chaque Saison, tous les Héros retrouvent leurs 9 Vies.

> Extrait de la messagerie du studio : « Les responsables de l'équilibrage veulent savoir où et comment les Héros perdent leurs Vies, Saison après Saison. C'est la première question qu'on nous pose après chaque mise à jour. »

## Les Pelotes d'or

La monnaie de Félicia est la **Pelote d'or**. Elle se gagne en accomplissant des quêtes ou en revendant des Trésors, et se dépense à la boutique ou en cotisation de Clan ; on peut aussi en acheter avec de l'argent réel. Chaque mouvement est conservé avec sa date, son montant et son motif. Une bourse ne descend jamais sous zéro.

> Extrait de la messagerie du studio : « Un Joueur qui achète des Pelotes d'or avec sa carte bancaire veut les retrouver sur son Héros préféré. »

::: encadre
Les Pelotes d'or ne sont pas dans l'atelier de la Séance 1 : on les retrouve en Séance 2, dans la base de données du module.
:::

## Ce que le studio veut pouvoir faire

Le modèle complet doit permettre de répondre, entre autres, aux demandes ci-dessous. L'atelier de la Séance 1 n'en couvre qu'une partie : la fin de chaque ligne le précise.

1. Afficher le **profil d'un Héros** : son Joueur, sa Lignée et ce qui la distingue, son niveau, son Clan, ses Vies restantes pour la Saison en cours et ses Trésors. *Dans l'atelier.*
2. Savoir **où et comment les Héros perdent leurs Vies**, par Île, par zone, par cause et par Saison. *Dans l'atelier.*
3. Établir le **classement de la Saison** : les Héros sont classés selon leur Renommée. *Hors atelier : la Renommée n'est pas à modéliser en Séance 1, le classement revient en Séance 3.*
4. Retrouver les **Clans alliés** d'un Clan, et les alliés de ses alliés. *Dans l'atelier, seulement si le temps le permet : l'alliance est facultative ; la recherche des alliés de ses alliés revient en Séance 3.*
5. Savoir **qui possède aujourd'hui** chaque Trésor légendaire. *Dans l'atelier.*

## Le rendu de l'atelier

::: bloc
En binôme, à partir de ce cahier des charges :

1. le **MCD** de Félicia dans Looping (ou Mocodo en ligne), limité à six concepts : **Joueur, Héros, Lignée, Clan, Trésor et Vies** ;
2. à côté du MCD, les **règles de gestion** qu'il ne montre pas, dont celle des 9 Vies ;
3. au moins **trois ambiguïtés** repérées, avec l'hypothèse retenue pour chacune, en une ligne.

Le studio vous enverra deux demandes en cours de route : les **Tickets du Game Designer**. Votre modèle devra s'adapter.

Ne sont **pas demandés** pendant l'atelier : les attributs propres à chaque nature de Trésor, la Renommée, les Pelotes d'or, les types de données des attributs, le niveau minimum des Îles et les dates des Saisons.
:::

### Par où commencer

- Mon conseil : partagez-vous le travail. L'un saisit le MCD, l'autre écrit au fur et à mesure les règles de gestion et les hypothèses, et vous échangez à chaque Ticket.
- Les Îles, leurs zones et les Saisons ne sont pas à modéliser : recopiez les éléments fournis ci-dessous et reliez-y vos entités quand le cahier des charges le demande (le repaire d'un Clan, l'obtention d'un Trésor, une Vie perdue). L'Île est déjà dans votre fichier depuis l'apport théorique (l'obtention d'un Trésor) : sous Windows, il reste à dessiner dans Looping la zone, la Saison et l'association COMPRENDRE.
- Les fragments dessinés pendant l'apport théorique (les Lignées, le mentorat, l'obtention d'un Trésor sur une Île) se reprennent tels quels.
- L'ordre que je vous conseille : Joueur, Héros et Lignées ; le mentorat ; les Trésors ; les Clans ; les Vies.
- Le chef d'un Clan et les alliances entre Clans viennent en dernier, si le temps le permet.

### Les éléments fournis

![Les Îles, leurs zones et les Saisons, réduites à leur identifiant et à leur nom pour l'atelier](felicia-elements-fournis.svg)

Une zone est identifiée par son nom **et** par son Île : c'est ce que dit le soulignement de la patte entre ZONE et COMPRENDRE (identification relative). Sous Mac et Linux, voici le texte Mocodo. Collez-le **sans sa première ligne** si votre fichier contient déjà l'Île : Mocodo refuse une entité déclarée deux fois (« Duplicate entity »).

```text
ÎLE: id_ile [INTEGER], nom_ile [VARCHAR(40)]
COMPRENDRE, 1N ÎLE, _11 ZONE
ZONE: nom_zone [VARCHAR(40)]

SAISON: id_saison [INTEGER], nom_saison [VARCHAR(40)]
```
