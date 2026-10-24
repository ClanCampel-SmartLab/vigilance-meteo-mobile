<p align="center"><img src="assets/icon.png" width="220" alt="Vigilance météo mobile — by clan'campel"></p>

# Vigilance météo mobile
### by clan'campel · ClanCampel — SmartLab

Notifications météo individuelles dans Home Assistant, selon le département de la dernière position géocodée du téléphone.

> Version 0.1.0-beta.2 expérimentale. Ce dépôt est un logiciel tiers, non affilié à Météo-France, Home Assistant ou HACS.
> Les tests purs et la syntaxe ont été vérifiés, mais l'intégration n'a pas encore été exécutée dans un véritable Home Assistant.
> Consulter https://vigilance.meteofrance.fr/ pour les informations officielles. Ne pas utiliser comme unique dispositif d'alerte.

## Ce que fait cette version

- Configuration dans l'interface, sans modifier configuration.yaml.
- Plusieurs destinataires, chacun avec son capteur géocodé et son action Companion.
- Un bulletin national partagé entre les destinataires.
- Département calculé séparément pour chaque téléphone : pas besoin de créer une météo par département.
- Icône dynamique du phénomène le plus élevé ; icône d'alerte si plusieurs phénomènes sont à égalité.
- Couleur dynamique du niveau maximal (rendu dépendant d'Android).
- Exclusions facultatives : AUCUN département exclu par défaut.
- Automatique désactivé par défaut, seuil jaune et intervalle de 30 minutes.
- Test manuel, capteur par destinataire et mémorisation du dernier bulletin envoyé.
- Pas de téléphone préconfiguré, pas de clé API fournie, pas d'annonce d'enceinte.

## Commencer ici

1. [Guide complet : préparer Companion, capteurs et notifications](docs/INSTALLATION.md).
2. [API Météo-France : obtenir et protéger sa clé](docs/API.md).
3. [Options, tests, exemples et limites](docs/UTILISATION.md).
4. [Dépannage pas à pas](docs/DEPANNAGE.md).
5. [Publier ce dépôt sur GitHub et installer avec HACS](docs/PUBLICATION.md).
6. [État réel des vérifications](VALIDATION.md).

## Prérequis

- Home Assistant Core 2026.3 ou plus récent : minimum déclaré et cible, non matrice de compatibilité testée.
- HACS déjà installé si vous choisissez ce mode d'installation ; installation locale également possible.
- Application officielle Home Assistant Companion sur chaque téléphone, connectée au BON serveur.
- Capteur Geocoded location activé sur chaque téléphone et envoyé au serveur concerné.
- Action `notify.mobile_app_…` du téléphone fonctionnelle.
- Clé API Météo-France autorisée pour le bulletin Vigilance et accès Internet depuis Home Assistant.

## Installation rapide après publication

1. Attendre la réussite de l'action GitHub « Préparer les métadonnées GitHub ».
2. Ajouter l'URL de VOTRE dépôt à HACS comme dépôt personnalisé, catégorie Intégration.
3. Télécharger l'intégration et redémarrer Home Assistant.
4. Paramètres → Appareils et services → Ajouter une intégration → Vigilance météo mobile.
5. Saisir la clé API, conserver l'automatique désactivé, laisser les exclusions vides si vous n'en voulez pas.
6. Ajouter chaque téléphone en associant le BON capteur à la BONNE action de notification ; terminer et enregistrer.
7. Tester, puis activer l'automatique dans les options seulement après validation.

## Test manuel

Dans Outils de développement → Actions :

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Ce test concerne tous les destinataires configurés. Il respecte toujours les exclusions et les positions inconnues.
Pour un seul téléphone, voir [le guide d'utilisation](docs/UTILISATION.md).

## Exemple de notification

```text
Vigilance météo : Département (XX).
Niveau maximal du bulletin d'aujourd'hui : jaune.
Vent violent : jaune du 24/10 à 20:00 au 25/10 à 00:00.
Bulletin selon votre dernière position connue.
Bulletin mis à jour : …
```

Le niveau est le maximum du bulletin d'aujourd'hui : ce n'est pas nécessairement le niveau à cet instant.

## Limites à lire avant activation

Métropole et Corse, bulletin J uniquement. Les zones littorales séparées et l'outre-mer NE SONT PAS pris en charge.
Les créneaux déjà passés du bulletin peuvent être affichés. La position utilisée est la dernière remontée ; son âge GPS n'est pas contrôlé.
Une position disponible peut être ancienne. L'affichage d'icône/couleur dépend du téléphone ; iOS n'offre pas le même rendu qu'Android.
La correspondance de département exige les attributs `iso_country_code` et `sub_administrative_area` attendus.
Les formats non conformes de capteur, notamment selon les versions iOS, ne sont pas garantis et seront ignorés.

## Confidentialité

La clé API reste dans la configuration locale Home Assistant, sans chiffrement supplémentaire par cette intégration.
L'intégration n'envoie ni l'adresse ni les coordonnées GPS à Météo-France : elle télécharge le bulletin national.
Companion utilise ses propres mécanismes de localisation, géocodage et notification ; cela ne signifie donc pas « aucune donnée ne quitte le téléphone ».
Protéger Home Assistant, les sauvegardes, .storage et secrets.yaml. Ne pas partager d'adresse ou de clé dans les tickets GitHub.

## Développement et licence

```bash
python tests/run.py
python -m compileall -q custom_components tools tests
```

Les tests ne simulent pas l'ensemble de Home Assistant. Les workflows de validation HACS/hassfest sont fournis, à exécuter et corriger si nécessaire avant diffusion.

Code sous licence MIT. Identité visuelle : « by clan'campel ». Source des données : Météo-France, soumise à ses propres conditions d'utilisation.
