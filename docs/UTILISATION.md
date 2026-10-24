# Utilisation, boutons et réglages

## Réglages avancés

| Option | Défaut | Description |
|---|---|---|
| Actualisation | 30 minutes | 15 à 1440 ; respecter les quotas et le délai accepté. |
| Niveau minimum automatique | Jaune | Vert, jaune, orange ou rouge. Test manuel indépendant du seuil. |
| Départements exclus | Vide | Liste commune, facultative. Codes séparés par des virgules. |
| Automatique | Désactivé | Activer volontairement après les tests ; peut envoyer un bulletin immédiatement. |

Modifier depuis l'entrée → Configurer/Options. Ajouter/modifier/retirer un profil puis terminer le récapitulatif.
Les options ne sont enregistrées qu'après sa validation. Le rechargement peut actualiser puis notifier si l'automatique est activé.

## Position et destinations : deux notions

Un profil = UNE position suivie + UNE OU PLUSIEURS destinations recevant le même bulletin.
Pour Papa et Maman en déplacements séparés : créer deux profils, une position personnelle pour chacun.
Pour copier le bulletin de Papa sur les deux téléphones : choisir la position de Papa et cocher les deux actions dans son profil.
Si une même destination figure dans plusieurs profils, elle peut recevoir plusieurs bulletins : c'est volontaire.

## Fiches et boutons

Une fiche centrale Vigilance météo mobile contient Actualiser le bulletin.
Chaque profil a une fiche virtuelle Vigilance météo — Nom : capteur et bouton Envoyer une notification de test.
Ces fiches représentent l'intégration et ses profils, pas un nouvel appareil physique installé sur le téléphone.
La page d'intégration n'est pas modifiée pour y injecter arbitrairement un gros bouton : ouvrir la fiche du profil et ses contrôles.
Le bouton test envoie à toutes les destinations du profil, pas aux autres profils.
Le bouton Actualiser peut déclencher les règles automatiques si elles sont activées.

## Tests via actions, si souhaité

Tous les profils :

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Un profil : copier son attribut recipient_id depuis son capteur, puis :

```yaml
action: vigilance_meteo_mobile.test
data:
  recipient_id: IDENTIFIANT_DU_PROFIL
```

Actualiser :

```yaml
action: vigilance_meteo_mobile.refresh
data: {}
```

Le test ignore seuil et désactivation automatique, mais respecte TOUJOURS position inconnue, exclusions, pays/zone non reconnus et validité du bulletin.
Il ne modifie pas la mémoire des alertes automatiques. Il envoie un vrai message TEST et ne garantit ni livraison physique ni lecture.
Le dernier test est conservé en mémoire dans les attributs last_test_status et last_test_time ; il peut disparaître au rechargement.
L'état du bouton indique sa dernière pression, PAS une confirmation de livraison.

## Résultats

L'action retourne éventuellement les résultats par profil et par destination.
L'événement vigilance_meteo_mobile_result les expose aussi. Le capteur expose le dernier statut de test.

- test_envoye / envoye : appels de notification acceptés.
- position_inconnue : entité absente, unknown ou unavailable.
- departement_non_pris_en_charge : pays, attributs ou territoire non reconnus.
- departement_exclu : exclusion choisie ; les données peuvent rester visibles dans la carte mais l'envoi est bloqué.
- bulletin_perime / bulletin_invalide / departement_absent / api_indisponible : pas d'envoi à partir de données inutilisables.
- sous_le_seuil / automatique_desactive / deja_envoye : règle automatique empêchant l'envoi.
- resultat_partiel : destinations avec résultats différents ; consulter leur détail.
- action_notification_absente / erreur_notification : action introuvable ou erreur pendant l'appel.

## Déduplication

Dernière signature par profil ET destination, enregistrée dans .storage.
Inclut département, période, niveau et créneaux, pas seulement l'heure de publication.
Une nouvelle journée, un changement de département ou de niveaux/horaires peut notifier.
Ce n'est pas un historique illimité ni un mécanisme de rappel d'urgence.
Après migration depuis bêta 2, une première notification peut être renvoyée du fait du nouveau format par destination.
Les tags remplacent visuellement le message précédent du profil, sans garantir absence de son/vibration.

## Limites

- Métropole et Corse, zones départementales, bulletin J seulement.
- Pas d'outre-mer ni de sous-zones littorales séparées ; ne pas revendiquer une couverture complète vagues-submersion.
- Maximum du bulletin d'aujourd'hui, pas nécessairement la vigilance maintenant. Des créneaux passés peuvent encore être affichés.
- Horaires selon le fuseau Home Assistant, pas forcément celui du téléphone.
- Pas de contrôle fiable de l'âge GPS. Une position disponible peut être ancienne.
- Formats iOS non reconnus ignorés ; rendu icône/couleur Android dépend du système et n'est pas identique à iOS.
- Pas de plages silencieuses, confirmations de lecture, annonce Google ni carte imposée automatiquement.
- Sans garantie de disponibilité API, accès distant ou notification.

## Configuration fermée accidentellement

Le formulaire affiche des avertissements et un récapitulatif. Il n'intercepte PAS le clic extérieur du frontend.
Fermer avant validation abandonne les changements non enregistrés ; l'ancienne configuration enregistrée reste intacte.
Un vrai dialogue de confirmation de fermeture demanderait un mécanisme frontend distinct : ce n'est pas implémenté ici.
