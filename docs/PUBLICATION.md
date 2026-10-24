# Mettre à jour le dépôt existant et publier la bêta 3

NE PAS supprimer le dépôt GitHub ni l'entrée Home Assistant.
Cette archive est reconstruite à partir du contenu fourni de la bêta 2 et des retours, pas téléchargée depuis votre branche actuelle.
Elle inclut les métadonnées connues de ClanCampel-SmartLab/vigilance-meteo-mobile et le workflow verification.yml.
Vérifier vos éventuelles modifications personnelles avant remplacement.

## 1. Préparer

1. Conserver une copie locale du dépôt et sauvegarder Home Assistant.
2. Désactiver temporairement l'automatique dans les options de l'intégration existante.
3. Décompresser l'archive bêta 3.
4. Copier son CONTENU à la racine du même dépôt, pas le ZIP ni un niveau parent supplémentaire.
5. Remplacer les fichiers existants et ajouter les nouveaux : button.py, entity.py, discovery.py, guides, exemples et tests.
6. Inclure .github/workflows et .gitignore : les noms commençant par un point peuvent être cachés dans l'explorateur.

Le workflow .github/workflows/verification.yml est bien inclus, vérifiable dans CONTENU_ARCHIVE.txt.
Si l'interface Web ne téléverse pas les dossiers cachés, utiliser GitHub Desktop/git ou créer le fichier à son chemin exact sur GitHub.
Si vous conservez d'anciens workflows tests.yml ou prepare-repository.yml, ils peuvent lancer des contrôles redondants ; verification.yml regroupe ces fonctions.

## 2. Vérifier GitHub

Faire le commit, puis Actions → Préparation du dépôt et tests.
Tests de syntaxe, logique et runtime SIMULÉ ; le job métadonnées utilise le vrai propriétaire/dépôt et ne modifie que le manifeste si nécessaire.
Les URLs sont déjà correctes pour ce dépôt. En cas de fork, elles peuvent être modifiées avec :

```bash
python tools/prepare_repository.py PROPRIETAIRE/DEPOT
```

Le workflow n'est pas exécuté automatiquement sur un fork. Aucun accès au compte GitHub n'est utilisé par l'archive en dehors des workflows que vous publiez.
L'archive ne publie rien ni ne crée de release à votre place.

## 3. Nouvelle release

Ne pas déplacer le tag v0.1.0-beta.2 existant.
Créer une NOUVELLE release ciblant le commit actuel de main : tag v0.1.0-beta.3, titre v0.1.0-beta.3 — Configuration simplifiée et boutons de test.
Cocher Préversion. Le manifeste contient version 0.1.0-beta.3.
Inutile d'ajouter le ZIP complet comme asset : HACS utilise le code du dépôt dans sa structure habituelle.
Une release de test n'est pas une certification HACS ni une preuve de fonctionnement réel.

## 4. Mise à jour HACS et retest

1. Dans HACS, ouvrir le dépôt et actualiser les informations si nécessaire.
2. Choisir la préversion v0.1.0-beta.3 dans le téléchargement / autre version si elle n'est pas proposée par défaut.
3. Télécharger puis redémarrer Home Assistant.
4. Vérifier les options existantes : la migration de version de config 1 vers 2 convertit notification en notifications.
5. Les identifiants de profils existants sont conservés par la conversion ; les boutons et appareils sont nouveaux.
6. Vérifier liens API via Reconfigurer, liste de positions et récapitulatif via Options.
7. Tester d'abord UN profil puis l'autre. Vérifier aussi les exclusions et la position inconnue.
8. Réactiver l'automatique seulement après validation ; une première nouvelle alerte peut être envoyée après migration.

## 5. Validation pour distribution

Le workflow manuel validate.yml lance HACS Action et hassfest. Il n'a pas été exécuté lors de cette génération.
Il n'ignore plus le contrôle brands ; certaines validations/catalogues peuvent demander des adaptations supplémentaires malgré les images locales.
Corriger les erreurs avant demande de référencement HACS. La coche des tests locaux ne suffit pas.
Tester configuration, options, migration réelle, appels API, notifications, déchargement, redémarrage et rendu de carte dans Home Assistant.
Ne pas annoncer cette bêta comme validée ni promettre une confirmation de fermeture non implémentée.

## Désinstallation si nécessaire

Supprimer l'entrée depuis Home Assistant puis les fichiers via HACS, redémarrer et vérifier les entités/appareils orphelins.
Le stockage .storage de déduplication peut subsister. Ne pas éditer .storage à chaud ni sans sauvegarde.
Révoquer la clé si elle ne sert plus. Ne pas supprimer le dépôt pour désinstaller une instance locale.
