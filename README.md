<p align="center">
  <img src="https://raw.githubusercontent.com/ClanCampel-SmartLab/vigilance-meteo-mobile/main/assets/icon.png" width="200" alt="Vigilance météo mobile — by clan'campel">
</p>

<h1 align="center">Vigilance météo mobile</h1>
<p align="center"><strong>Vos alertes météo vous accompagnent dans vos déplacements.</strong></p>
<p align="center">Une intégration Home Assistant signée <strong>ClanCampel — SmartLab</strong> </p>

<p align="center">
  <a href="https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/releases"><img src="https://img.shields.io/github/v/release/ClanCampel-SmartLab/vigilance-meteo-mobile?label=version" alt="Dernière version publiée"></a>
  <a href="https://www.home-assistant.io/"><img src="https://img.shields.io/badge/Home%20Assistant-2026.3%2B-18BCF2" alt="Home Assistant 2026.3 ou supérieur"></a>
  <a href="https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/LICENSE"><img src="https://img.shields.io/badge/licence-MIT-green" alt="Licence MIT"></a>
</p>

---

## 🌦️ La vigilance météo, là où vous êtes

Vous voyagez, partez en week-end ou vous déplacez pour le travail ? Recevez les bulletins de vigilance Météo-France correspondant au département de votre dernière position connue, directement sur votre téléphone.

Chaque personne peut suivre sa propre position. Si deux téléphones se trouvent dans des départements différents, chacun reçoit les informations de son profil — sans créer un capteur météo pour chaque destination.

La configuration se fait dans l’interface Home Assistant : pas de script à écrire, pas de `rest_command` à ajouter, pas de modification de `configuration.yaml` ou de `secrets.yaml`.

## ✨ Fonctionnalités

- **Position individuelle** : département identifié depuis le capteur géocodé de l’application Companion.
- **Plusieurs profils** : un téléphone ou une position à suivre par profil.
- **Destinations multiples** : possibilité de partager le bulletin d’une même position avec plusieurs téléphones.
- **Notifications lisibles** : département, niveau maximal du bulletin, phénomènes et créneaux horaires.
- **Icône et couleur dynamiques** : selon le phénomène et la vigilance, sous réserve du rendu du téléphone.
- **Seuil configurable** : notifications automatiques à partir du niveau choisi.
- **Exclusions facultatives** : aucun département exclu par défaut.
- **Actualisation partagée** : un bulletin national téléchargé pour l’ensemble des profils.
- **Limitation des doublons** : mémoire de la dernière signature envoyée par profil et destination.
- **Test individuel** : bouton accessible dans la fiche du profil.
- **Tableau de bord** : capteur détaillé et exemple de carte native, sans extension frontend obligatoire.

## 📱 Avant de commencer

Vous avez besoin de :

| Prérequis | À vérifier |
|---|---|
| Home Assistant | Version 2026.3 ou supérieure déclarée par le projet. |
| Application Companion | Connectée au serveur Home Assistant qui exécutera l’intégration. |
| Localisation géocodée | Capteur **Geocoded location** activé et envoyé à ce serveur. |
| Notifications | Action `notify.mobile_app_…` du téléphone testée. |
| Accès Météo-France | Clé API autorisée pour l’API Vigilance / DPVigilance. |
| Connexion | Accès Internet depuis Home Assistant ; accès au serveur depuis le téléphone en déplacement. |

👉 [Guide complet : Companion, autorisations, capteurs et notifications](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/docs/INSTALLATION.md)

👉 [Comment obtenir votre clé API Météo-France](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/docs/API.md)

## 📦 Installation avec HACS

### Ajouter le dépôt

Tant que le projet n’est pas accepté au catalogue HACS par défaut :

1. Ouvrez **HACS** dans Home Assistant.
2. Ouvrez le menu des **dépôts personnalisés**.
3. Ajoutez cette URL, catégorie **Intégration** :

```text
https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile
```

4. Recherchez **Vigilance météo mobile** et téléchargez la version publiée.
5. Redémarrez Home Assistant.

L’installation dans HACS télécharge les fichiers ; elle ne remplace pas l’étape de configuration ci-dessous.

### Configurer l’intégration

1. Ouvrez **Paramètres → Appareils et services → Ajouter une intégration**.
2. Recherchez **Vigilance météo mobile**.
3. Saisissez votre clé API. Des liens vers le guide et le portail Météo-France sont disponibles sur cette page.
4. Ajoutez un profil et sélectionnez la position géocodée du téléphone dans la liste.
5. Choisissez sa ou ses destinations de notification.
6. Donnez-lui un nom si vous le souhaitez : **Papa**, **Maman**, **Téléphone personnel**… Sinon, le nom du téléphone est utilisé.
7. Ajustez les réglages avancés si nécessaire.
8. Relisez le récapitulatif puis validez l’enregistrement.

**Important :** une position avec deux destinations envoie le même bulletin aux deux téléphones. Pour deux personnes pouvant voyager séparément, créez deux profils avec leurs positions respectives.

Les changements ne sont enregistrés qu’à la validation finale. Fermer la fenêtre avant cette étape abandonne les changements non enregistrés.

## ⚙️ Réglages

| Réglage | Valeur initiale | Fonction |
|---|---|---|
| Notifications automatiques | Désactivées | Permet de tester avant tout envoi automatique. |
| Niveau minimum | Jaune | Seuil des notifications automatiques. |
| Actualisation | 30 minutes | Configurable de 15 à 1440 minutes, selon vos quotas et le délai accepté. |
| Départements exclus | Aucun | Liste facultative commune aux profils. |
| Destinataires | Aucun | À ajouter et associer explicitement. |

Les options permettent ensuite d’ajouter, de modifier ou de retirer des profils. Activer l’automatique peut déclencher un premier envoi dès l’enregistrement.

## 🔔 Tester une notification

1. Ouvrez l’intégration dans **Appareils et services**.
2. Ouvrez la fiche **Vigilance météo — Nom du profil**.
3. Appuyez sur **Envoyer une notification de test**.
4. Vérifiez le téléphone destinataire, le département et les horaires.

Le bouton envoie un vrai message de test aux destinations de ce profil. Il fonctionne même si l’automatique est désactivé, mais respecte les exclusions, les positions inconnues et la validité du bulletin.

Vous pouvez également tester tous les profils depuis les outils de développement :

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Pour cibler un seul profil, renseignez son attribut `recipient_id` :

```yaml
action: vigilance_meteo_mobile.test
data:
  recipient_id: IDENTIFIANT_DU_PROFIL
```

Le bouton commun **Actualiser le bulletin** récupère les données. Si les notifications automatiques sont activées, les règles habituelles peuvent provoquer un envoi.

## 🧭 Exemple de message

```text
Vigilance météo : Morbihan (56).
Niveau maximal du bulletin d’aujourd’hui : jaune.
Vent violent : jaune du 24/10 à 20:00 au 25/10 à 00:00.
Bulletin selon votre dernière position connue.
Bulletin mis à jour : …
```

Le niveau affiché est le maximum du bulletin d’aujourd’hui, pas nécessairement celui en cours à l’instant de la notification.

## 🏠 Votre tableau de bord

Ajoutez le capteur du profil et ses boutons à votre tableau de bord avec les cartes natives Home Assistant.

La carte détaillée proposée présente :

- Le nom du profil.
- Le département et son code, sans adresse précise.
- Le niveau de vigilance.
- Les phénomènes et leurs horaires.
- Le statut des données et le dernier résultat de test.
- Les boutons de test et d’actualisation.

👉 [Guide et adaptation des identifiants d’entités](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/docs/TABLEAU_DE_BORD.md)

👉 [Exemple complet de carte native](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/examples/carte-vigilance.yaml)

Aucun tableau de bord n’est créé ou modifié automatiquement.

## 🔒 Vos données

- La clé API reste dans la configuration locale Home Assistant ; cette intégration n’ajoute pas de chiffrement spécifique.
- Protégez l’accès à Home Assistant et ses sauvegardes, qui peuvent contenir vos secrets.
- L’intégration télécharge le bulletin national et ne transmet pas votre adresse ou vos coordonnées GPS à Météo-France.
- Companion conserve ses propres mécanismes de localisation, de géocodage et de notification : le fonctionnement n’est pas entièrement local.
- Ne publiez pas de clé, d’adresse, de coordonnées ou de sauvegarde dans un ticket GitHub.

## ℹ️ Couverture et points à connaître

- **France métropolitaine et Corse uniquement.** Pas d’outre-mer dans cette version.
- **Zones départementales uniquement.** Les sous-zones littorales séparées ne sont pas traitées : aucune couverture complète des vagues-submersion n’est revendiquée.
- **Bulletin d’aujourd’hui uniquement.** Des créneaux déjà passés dans la journée peuvent encore apparaître.
- **Dernière position connue.** Une position disponible peut être ancienne ; l’âge réel du relevé GPS n’est pas contrôlé.
- **Horaires du serveur.** Les créneaux sont convertis selon le fuseau configuré dans Home Assistant.
- **Compatibilité des capteurs.** Les attributs `iso_country_code` et `sub_administrative_area` sont attendus. Les variantes non reconnues, notamment selon iOS, sont ignorées.
- **Rendu du téléphone.** L’affichage des icônes et couleurs dépend du système ; iOS ne propose pas le même rendu qu’Android.
- **Notifications.** Un appel accepté ne garantit ni livraison physique ni lecture. Pas de rappels d’urgence, de plages silencieuses ou d’annonce d’enceinte intégrés dans cette version.

Cette intégration est indépendante et ne remplace pas les [bulletins officiels de Météo-France](https://vigilance.meteofrance.fr/) ni les consignes des autorités.

## 🛠️ Aide et contribution

- [Utilisation et résultats des tests](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/docs/UTILISATION.md)
- [Dépannage](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/docs/DEPANNAGE.md)
- [Historique des versions](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/CHANGELOG.md)
- [Signaler un problème](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/issues)

Pour un signalement, indiquez les versions Home Assistant, Companion et de l’intégration, les étapes suivies et l’erreur pertinente, sans données privées.

### Développement

```bash
python tests/run.py
python -m compileall -q custom_components tools tests
```

Le dépôt fournit des tests de logique, des tests avec environnement simulé et un workflow manuel HACS/hassfest. Les résultats de ces contrôles sont à distinguer des essais réels et de l’acceptation au catalogue HACS.

## 📜 Licence et crédits

Code et ressources du projet sous [licence MIT](https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile/blob/main/LICENSE).
Données de vigilance : **Météo-France**, selon ses conditions d’utilisation.
Projet indépendant, non affilié à Météo-France, Home Assistant ou HACS.

<p align="center">Conçu par <strong>by clan'campel</strong><br>ClanCampel — SmartLab</p>
