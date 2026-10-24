# Installation détaillée — depuis le téléphone

Les intitulés changent selon Android/iOS, la langue, la version de Companion et de Home Assistant.
Ne sautez pas les étapes de test : une entité activée dans Home Assistant ne garantit pas que le téléphone lui envoie des données.

## 1. Choisir le bon serveur

1. Ouvrir l'application officielle Home Assistant Companion sur le téléphone.
2. Ajouter/connecter l'instance qui exécutera cette intégration.
3. Avec plusieurs maisons/serveurs, sélectionner le bon serveur dans les réglages et le tableau de bord.
4. Vérifier que l'appareil du téléphone apparaît dans Paramètres → Appareils et services → Mobile App sur CE serveur.
5. Vérifier que le téléphone peut joindre ce serveur aussi hors du Wi-Fi si vous voulez les mises à jour en déplacement.

Ne publiez pas votre Home Assistant sur Internet sans configuration sécurisée. Utiliser une méthode d'accès distant appropriée.

## 2. Android : autorisations et capteur géocodé

1. Sur le téléphone, ouvrir les paramètres Android de l'application Home Assistant.
2. Autoriser les notifications. Autoriser la localisation précise et l'accès en arrière-plan si Android le propose et si vous acceptez cet usage.
3. Vérifier que la localisation du téléphone est activée.
4. Dans Companion : Paramètres → Application Companion → Gérer les capteurs (Manage sensors).
5. Rechercher « Geocoded location » / « Localisation géocodée » ou le libellé approchant.
6. Ouvrir sa fiche et activer le capteur.
7. Avec plusieurs serveurs, ouvrir les réglages par serveur du capteur (icône d'expansion en haut selon la version) et activer l'envoi vers le serveur voulu.
8. Dans les capteurs de localisation, vérifier « Background Location » / localisation en arrière-plan. Ce réglage est distinct du capteur géocodé.
9. Vérifier que les réglages de confidentialité n'interdisent pas l'envoi des capteurs au serveur.
10. Rouvrir l'application et laisser le temps à une mise à jour de se faire ; vérifier ensuite les valeurs côté Home Assistant.

Il n'est pas nécessaire d'activer le mode GPS haute précision permanent : il peut augmenter fortement la consommation.
Si les données cessent de remonter en arrière-plan, consulter les règles d'économie de batterie de votre constructeur et la documentation Companion.
N'activer que les permissions nécessaires et comprises.

## 3. iPhone : autorisations et vérification de compatibilité

1. Réglages iOS → Applications → Home Assistant (ou Réglages → Home Assistant selon iOS).
2. Autoriser les notifications. Pour le suivi en arrière-plan, vérifier les autorisations de localisation, notamment « Toujours » et « Position exacte », si proposées.
3. Dans Companion : Paramètres → Application Companion → Capteurs (Sensors).
4. Avec plusieurs serveurs, sélectionner le serveur concerné.
5. Activer « Geocoded location » / localisation géocodée et vérifier les options de confidentialité d'envoi des capteurs.
6. Revenir au tableau de bord, l'actualiser et vérifier le capteur côté serveur.

iOS décide en partie des moments de mise à jour. Il ne s'agit pas d'un suivi instantané garanti.
IMPORTANT : cette bêta attend `iso_country_code` et `sub_administrative_area`. Vérifier ces attributs ; tous les formats iOS ne sont pas encore pris en charge.
Le rendu de l'icône/couleur Android n'est pas garanti sur iPhone.

## 4. Retrouver le capteur dans Home Assistant

1. Sur le BON serveur, ouvrir Outils de développement → États.
2. Filtrer les entités avec `geocoded` (ou rechercher le nom du capteur de localisation).
3. Identifier le téléphone grâce à la colonne Appareil et à son nom.
4. Copier l'identifiant complet, par exemple `sensor.mon_telephone_geocoded_location`.
5. Vérifier qu'il n'est ni `unknown` ni `unavailable`.
6. Vérifier dans les attributs :

```yaml
iso_country_code: FR
sub_administrative_area: Morbihan
```

Ceci est un exemple, pas une configuration à coller. Le nom du département doit correspondre à votre position.
Le capteur géocodé n'est pas `device_tracker.…`. Le tracker ne fournit pas forcément le nom du département attendu.
Ne publiez pas la capture complète de l'adresse du capteur.

Si l'entité est désactivée dans Home Assistant : Paramètres → Appareils et services → Entités → filtrer les entités désactivées,
retrouver celle du téléphone et l'activer. Il faut AUSSI avoir activé le capteur dans Companion.

## 5. Retrouver l'action de notification

Il s'agit d'une ACTION, pas d'un capteur de notification.

1. Ouvrir Outils de développement → Actions (anciennement Services).
2. Rechercher `notify.mobile_app_`.
3. Repérer l'action du téléphone, par exemple `notify.mobile_app_mon_telephone`.
4. Passer en édition YAML si souhaité et adapter :

```yaml
action: notify.mobile_app_mon_telephone
data:
  message: "Test de notification Home Assistant"
```

5. Cliquer sur Exécuter et vérifier physiquement quel téléphone reçoit le message.
6. Si le mauvais téléphone reçoit, corriger votre association avant de poursuivre.
7. Refaire le test pour chaque destinataire.

Le nom de l'action et celui du capteur ne sont pas obligatoirement identiques. Ne pas les deviner.
`notify.send_message` est une autre interface ; cette bêta demande l'action Companion `notify.mobile_app_…` pour les données avancées.
Dans l'intégration, les actions Companion disponibles sont proposées dans une liste.

## 6. Installer l'intégration

### HACS, après publication du dépôt

1. S'assurer que HACS est déjà installé et fonctionnel.
2. Dans HACS, ouvrir le menu des dépôts personnalisés (emplacement variable selon version).
3. Ajouter l'URL du dépôt GitHub publié et choisir le type Intégration.
4. Ouvrir Vigilance météo mobile puis télécharger.
5. Redémarrer Home Assistant.
6. Paramètres → Appareils et services → Ajouter une intégration → chercher Vigilance météo mobile.

### Installation locale de validation

1. Sauvegarder Home Assistant.
2. Copier le dossier `custom_components/vigilance_meteo_mobile` de ce dépôt vers le dossier `custom_components` de la configuration Home Assistant.
3. Le résultat doit être `/config/custom_components/vigilance_meteo_mobile/manifest.json`, pas un double sous-dossier.
4. Redémarrer Home Assistant, puis ajouter l'intégration comme ci-dessus.

## 7. Configurer

1. Saisir la valeur de la clé API obtenue selon [API.md](API.md), sans `!secret`.
2. Choisir un intervalle respectant votre quota (30 minutes par défaut).
3. Choisir le seuil automatique (jaune par défaut).
4. Laisser les exclusions VIDES si vous ne voulez exclure aucun département.
5. Laisser l'automatique désactivé pendant les tests.
6. Ajouter un téléphone : nom libre, capteur géocodé exact et action Companion du même appareil.
7. Ajouter les autres téléphones si nécessaire.
8. Choisir Terminer et enregistrer. Quitter avant cette étape n'enregistre pas les modifications.
9. Tester selon [UTILISATION.md](UTILISATION.md), puis activer volontairement l'automatique dans les options.

## Documentation officielle

- Capteurs et réglages multi-serveurs : https://companion.home-assistant.io/docs/core/sensors/
- Localisation et permissions : https://companion.home-assistant.io/docs/core/location/
- Notifications : https://companion.home-assistant.io/docs/notifications/notifications-basic/
