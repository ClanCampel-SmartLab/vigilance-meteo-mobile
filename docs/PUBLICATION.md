# Publier la version 1.0.0 et demander le référencement HACS

## Fichiers de version

- custom_components/vigilance_meteo_mobile/manifest.json : version 1.0.0.
- custom_components/vigilance_meteo_mobile/const.py : VERSION = "1.0.0".
- README et guides : présentation courante, sans avertissements de préversion périmés.
- CHANGELOG : conserver l’historique réel des préversions, puis ajouter la version 1.0.0.
- hacs.json : pays FR et version Home Assistant minimale déclarée.

Le kit de publication ne remplace pas le code de l’intégration ni les derniers sensor.py/fr.json corrigés.
Il doit être fusionné dans le dépôt existant, pas téléversé comme nouveau projet complet.

## Avant la release

1. Committer les fichiers sur main.
2. Faire réussir Préparation du dépôt et tests.
3. Exécuter le workflow manuel Validation HACS et hassfest.
4. Vérifier que HACS Action passe sans erreurs ni contrôles ignorés, et hassfest passe.
5. Vérifier description du dépôt, topics, Issues activées, licence identifiable et images de marque.
6. Corriger tout défaut avant de demander le référencement. Des essais utilisateur ne remplacent pas ces validations.

Les tests réels de l’auteur et les contrôles automatisés sont distincts. Ne pas déclarer une acceptation HACS non obtenue.

## Release stable

Créer une NOUVELLE release GitHub : tag v1.0.0 sur le commit main validé, titre v1.0.0 — Vigilance météo mobile.
Ne PAS cocher Préversion. Définir comme Latest si proposé et approprié.
Ne pas déplacer les anciens tags ni effacer les préversions ; conserver l’historique et le retour arrière.
Pas besoin de joindre un ZIP du projet complet pour l’installation HACS standard.
Télécharger ensuite v1.0.0 depuis HACS et redémarrer pour confirmer le paquet réellement publié.

## Catalogue HACS par défaut

Se référer à https://hacs.xyz/docs/publish/include/ au moment de soumettre.

- Dépôt public, utilisable comme dépôt personnalisé.
- HACS Action réussie sans erreurs ni ignore, hassfest réussi.
- Nouvelle release publiée APRÈS réussite des validations.
- Entrée à ajouter dans le fichier integration de hacs/default, dans l’ordre alphabétique.
- Forker hacs/default et créer une branche depuis sa branche master, selon les consignes officielles en vigueur.
- Pull request remplie honnêtement, modifiable par les mainteneurs, déposée par propriétaire ou contributeur majeur.
- country dans le hacs.json publié pour un projet limité à certains pays.
- Description, topics, Issues et licence conformes ; marque et manifeste vérifiés.

Ne pas déclarer la validation HACS si elle n’a pas eu lieu. L’acceptation et les délais relèvent de HACS, pas du projet.
En attendant, conserver les instructions de dépôt personnalisé dans le README.

## Confidentialité et workflows

Ne jamais publier de clé ou de données personnelles.
Conserver les workflows de vérification et de validation du dépôt existant ; ce kit ne les remplace pas.
