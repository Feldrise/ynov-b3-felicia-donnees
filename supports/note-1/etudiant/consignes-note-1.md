---
title: Consignes de la Note 1
soustitre: Du cahier des charges au MCD et au MLD, avec un choix de dénormalisation justifié
surtitre: Note 1 · Séance 2 · Mardi 10 novembre, 10h30 à 11h45
public: Support étudiant
---

::: bloc
### La Note 1 en un coup d'œil

| | |
|--------------------|----------------------------------------------------------------|
| Quand | mardi 10 novembre, de **10h30 à 11h45** (1 h 15, dépôt compris) |
| Format | **individuel** |
| Poids | **40 %** de la moyenne du module |
| Sujet | une fonctionnalité d'**un autre jeu** que Félicia, distribuée à 10h30 |
| Autorisés | tous les documents, et le **Familier** |
| Rendu | un **dossier** à partir du modèle Word, et ton fichier Looping, sur **Moodle** avant 11h45 |
:::

## Ce que l'on évalue

Le sujet est un mini cahier des charges, avec des règles parfois implicites et une petite partie du MCD **fournie** : reprends-la telle quelle et relies-y le reste. Je note ton **jugement de conception**, pas ta vitesse de dessin.

| Critère | Points | Ce qui est attendu |
|---------------------------------------|--------|--------------------------------------------------------------|
| **MCD** | **40 points** | les bonnes entités et leurs identifiants ; des associations et des cardinalités justes, lues dans les deux sens ; les règles implicites du sujet repérées ; les règles de gestion que le schéma ne montre pas, écrites à côté |
| **MLD** | **20 points** | le MLD généré par Looping, **relu et corrigé** : clés primaires et étrangères correctes, rôles nommés, colonnes obligatoires et contraintes du sujet ajoutées ; une ligne par vérification ou correction |
| **Justification de la dénormalisation** | **25 points** | **un seul** choix, en 5 à 6 lignes, rattaché à une charge citée par le sujet ; le gain en lecture ; le coût en cohérence et en écriture ; qui maintient la copie, et quand |
| **Journal du Familier** | **15 points** | chaque prompt copié tel quel (ou un lien de partage), sa réponse en bref, et pour chacun : gardé, rejeté ou modifié, **parce que...**, en citant le sujet |

Pour la justification, reprends le raisonnement de l'atelier. Sans charge précise à soulager ni coût identifié, elle ne rapporte presque rien.

## Le Familier et les documents

Le **Familier** et tous les documents sont autorisés (supports, tes fichiers, Internet). Le **Journal du Familier** est **obligatoire** : il tient dans la dernière partie du dossier, une ligne par prompt. Remplis-le **au fil de l'eau**, pas à la fin. Sans Familier, explique pourquoi en deux ou trois lignes.

La Note est **individuelle** : aucune communication avec un autre étudiant, ni à voix haute ni par messagerie.

## Le déroulé conseillé

| Heure | Ce que tu fais |
|-------|------------------------------------------------------------------------|
| 10h30 | Lecture du sujet, crayon en main : souligne chaque règle et chaque chiffre. |
| 10h35 | MCD, à partir des éléments fournis ; règles de gestion dans le dossier. |
| 11h05 | MLD : génération, collage, relecture avec la grille en huit questions de la Séance 2. |
| 11h15 | Justification de la dénormalisation. |
| 11h30 | Relecture du Journal, dossier en PDF, dépôt. |
| 11h45 | Fin du dépôt sur Moodle. |

J'annonce l'heure à 11h15 et à 11h35. Rien à préparer avant.

## Le dossier et le dépôt sur Moodle

Tout s'écrit dans le **modèle de dossier**, `dossier-note-1-modele.docx`, à télécharger sur Moodle avant 10h30 (Word, LibreOffice Writer ou Google Docs). Colles-y l'image du MCD (Looping : copier le diagramme ; Mocodo en ligne : télécharger l'image) et le MLD généré. Deux fichiers à déposer, à ton nom et prénom :

1. `NOM-Prenom-note-1.loo` : le fichier Looping de ton MCD (sous Mocodo, ton texte Mocodo, `NOM-Prenom-note-1.mcd`) ;
2. `NOM-Prenom-note-1.pdf` : le dossier rempli, enregistré en PDF.

Un dépôt incomplet à 11h45 est corrigé tel quel : dépose une première version à 11h35, puis remplace-la si besoin.

## La grille de la Note 1 {.nouvelle-page}

La copie est notée sur 100 ; la note sur 20 est le total divisé par 5. Une **hypothèse écrite** et cohérente avec le sujet n'est jamais une faute : je corrige ton modèle au regard de ton hypothèse. La partie du MCD fournie par le sujet ne rapporte ni ne coûte de points.

| Critère | Ce qui est attendu | Points |
|--------------------------------|----------------------------------------------------------------------|--------|
| **MCD** | | **40** |
| Entités et identifiants | chaque entité du sujet, avec son identifiant et ses attributs ; la partie fournie reprise telle quelle | 7,5 |
| Associations et cardinalités | toutes les associations du sujet, avec des cardinalités justes lues dans les deux sens | 12,5 |
| Pièges de modélisation | le sujet en cache trois : chacun bien traduit dans le modèle rapporte 5 points | 15 |
| Règles de gestion écrites | au moins deux des règles implicites du sujet que le schéma ne montre pas, écrites à côté du MCD | 5 |
| **MLD** | | **20** |
| Règles de passage | une table par entité et par association N-N, les clés étrangères au bon endroit | 7,5 |
| Réflexive traduite | deux colonnes aux noms distincts, qui disent leur rôle | 2,5 |
| Relecture et corrections | au moins trois vérifications ou corrections notées ; un MLD rendu tel que généré, sans un mot, ne rapporte rien ici | 7,5 |
| Cohérence avec le MCD | ni table fantôme, ni table oubliée | 2,5 |
| **Justification de la dénormalisation** | | **25** |
| Un seul choix, rattaché au sujet | une dénormalisation précise, au service d'un écran ou d'une charge du sujet ; si tu en proposes plusieurs, seule la première est notée | 5 |
| Gain en lecture | ce que la lecture n'a plus à faire, expliqué | 7,5 |
| Coût en cohérence et en écriture | le risque de divergence et le surcoût à l'écriture, pesés contre la fréquence de la lecture | 7,5 |
| Maintenance de la copie | qui la tient à jour, et à quel moment | 5 |
| **Journal du Familier** | | **15** |
| Présence et forme | chaque prompt copié tel quel, avec la réponse en bref et ta décision | 5 |
| Décisions justifiées | chaque « parce que... » cite une règle, un chiffre ou une phrase du sujet | 7,5 |
| Regard critique | au moins un prompt rejeté ou modifié, avec une raison solide | 2,5 |
| **Total** | | **100** |

Sur chaque ligne, une réponse partielle rapporte la moitié des points. Journal absent : 0 sur ce critère. Sans Familier, ton explication remplace le Journal : 5 points pour sa présence, jusqu'à 10 pour sa qualité.
