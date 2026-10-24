<p align="center"><img src="assets/icon.png" width="220" alt="Vigilance météo mobile — by clan'campel"></p>

# Vigilance météo mobile
### by clan'campel · ClanCampel — SmartLab

Les alertes de vigilance Météo-France vous accompagnent dans vos déplacements, selon votre dernière position connue.
Intégration personnalisée pour Home Assistant. Aucun téléphone ni département exclu par défaut.

> Bêta 0.1.0-beta.3. Logiciel tiers, non affilié à Météo-France, Home Assistant ou HACS.
> Tests de logique et tests simulés réussis, mais cette version n'a pas encore été exécutée dans un vrai Home Assistant.
> Consulter https://vigilance.meteofrance.fr/ et les consignes des autorités. Ne pas utiliser comme unique système d'alerte.

## Nouveautés bêta 3

- Liens vers le guide et le portail API dès la saisie de la clé.
- Liste ciblée des capteurs géocodés avec nom lisible et disponibilité ; aide si aucun n'est trouvé.
- Nom facultatif : le nom du téléphone est utilisé par défaut, sans lien obligatoire avec une personne Home Assistant.
- Une ou plusieurs destinations de notification pour un même profil de position, avec avertissement explicite.
- Ajout, modification et suppression de profils ; récapitulatif final avant enregistrement.
- Réglages avancés séparés, aucune exclusion par défaut et automatique désactivé par défaut.
- Une fiche virtuelle par destinataire avec capteur détaillé et bouton de test individuel.
- Une fiche centrale avec bouton d'actualisation commun.
- Exemple de carte native pour tableau de bord, sans Mushroom ni extension frontend.
- Migration prévue des associations de la bêta 2, sans supprimer l'entrée ni saisir à nouveau la clé.

## Documentation

1. [Installer et préparer Companion, capteurs et notifications](docs/INSTALLATION.md).
2. [Obtenir et protéger la clé Météo-France](docs/API.md).
3. [Configurer, tester et comprendre les résultats](docs/UTILISATION.md).
4. [Ajouter une carte au tableau de bord](docs/TABLEAU_DE_BORD.md).
5. [Dépanner](docs/DEPANNAGE.md).
6. [Mettre le dépôt à jour et publier une release](docs/PUBLICATION.md).
7. [Vérifications effectuées et limites des tests](VALIDATION.md).

## Prérequis

- Home Assistant Core 2026.3+ : cible minimale déclarée, pas une matrice de compatibilité testée.
- Application officielle Home Assistant Companion, connectée au BON serveur, avec capteur géocodé et notifications.
- Clé API Météo-France autorisée pour DPVigilance / cartevigilance/encours.
- Accès Internet depuis Home Assistant.
- HACS pour l'installation via dépôt personnalisé, ou copie locale pour la validation.

## Installation HACS

Ajouter `https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile` comme dépôt personnalisé de type Intégration.
Télécharger la version souhaitée (sélectionner la préversion si nécessaire), puis redémarrer Home Assistant.
Paramètres → Appareils et services → Ajouter une intégration → Vigilance météo mobile.
Saisir la clé, ajouter les profils et terminer le récapitulatif. Laisser l'automatique désactivé pendant les essais.

## Mise à jour depuis la bêta 2

Ne pas supprimer le dépôt GitHub, l'intégration ni l'entrée Home Assistant.
Désactiver temporairement l'automatique dans les options, publier/télécharger la nouvelle version puis redémarrer.
Les associations existantes sont migrées vers une liste de destinations ; vérifier les options avant réactivation.
La migration du format est testée comme fonction pure, pas encore dans le cycle réel de Home Assistant.
La mémoire de déduplication étant désormais par destination, une première nouvelle notification automatique peut être envoyée après mise à jour.

## Tester sans YAML

Dans Appareils et services → Vigilance météo mobile, ouvrir la fiche virtuelle du destinataire.
Dans ses contrôles, appuyer sur « Envoyer une notification de test ».
Ce bouton envoie réellement aux destinations de CE profil. Il respecte les exclusions et les positions inconnues.
Le bouton central « Actualiser le bulletin » récupère les données et peut déclencher les règles automatiques si elles sont activées.

L'action existante reste disponible :

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Elle vise tous les profils, sauf si recipient_id est renseigné.

## Données et confidentialité

Métropole et Corse, bulletin J uniquement. Niveau maximal d'aujourd'hui, pas nécessairement celui de maintenant.
Sous-zones littorales et outre-mer non couverts. La dernière position peut être ancienne : l'âge GPS n'est pas contrôlé.
L'intégration lit les attributs `iso_country_code` et `sub_administrative_area` ; tous les formats iOS ne sont pas garantis.
Elle ne transmet pas l'adresse ou les coordonnées à Météo-France : téléchargement du bulletin national.
Companion garde ses propres mécanismes de géocodage et de notifications ; ce n'est pas une promesse de fonctionnement 100 % local.
La clé reste dans le stockage Home Assistant, sans chiffrement supplémentaire par cette intégration. Protéger accès et sauvegardes.
Aucune modification de configuration.yaml ou secrets.yaml, aucun script/automation créé, aucun tableau de bord modifié automatiquement.

## Fermeture du formulaire

Un récapitulatif et des avertissements clarifient l'enregistrement. Le clic extérieur est géré par Home Assistant.
L'intégration ne prétend PAS intercepter cette fermeture ou afficher une confirmation « fermer sans enregistrer ».
Les modifications ne sont conservées qu'après validation du récapitulatif final.

## Développement

```bash
python tests/run.py
python -m compileall -q custom_components tools tests
```

Les tests simulés utilisent des doubles de Home Assistant : ils ne garantissent ni la compatibilité frontend ni le chargement réel.
Les workflows HACS/hassfest sont fournis séparément, à exécuter. Le référencement au catalogue HACS n'est pas automatique.

Code et ressources sous licence MIT. Signature : by clan'campel. Les données Météo-France restent soumises à leurs conditions d'usage.
