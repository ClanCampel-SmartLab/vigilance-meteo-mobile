# Utilisation et réglages

| Option | Défaut | Fonction |
|---|---|---|
| Actualisation | 30 min | De 15 à 1440 minutes, selon quotas et délai accepté. |
| Seuil automatique | Jaune | Vert, jaune, orange ou rouge. |
| Exclusions | Aucune | Liste facultative de codes séparés par des virgules, commune aux profils. |
| Automatique | Désactivé | Activer après les essais ; peut provoquer un premier envoi immédiat. |

Options : ajout, modification et retrait de profils, puis enregistrement au récapitulatif final.
Un profil suit UNE position et notifie UNE OU PLUSIEURS destinations. Pour deux positions indépendantes, créer deux profils.

## Boutons

- Fiche centrale : Actualiser le bulletin. Peut déclencher les règles automatiques si activées.
- Fiche du profil : Envoyer une notification de test. Vise les destinations de ce profil seulement.

Les fiches sont virtuelles : elles ne correspondent pas à un nouvel appareil physique.
L’état d’un bouton est son heure de dernière pression, pas une preuve de réception.

## Actions

Tous les profils :

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Un profil :

```yaml
action: vigilance_meteo_mobile.test
data:
  recipient_id: IDENTIFIANT_COPIE_DANS_LES_ATTRIBUTS_DU_CAPTEUR
```

Actualiser :

```yaml
action: vigilance_meteo_mobile.refresh
data: {}
```

Le test envoie un vrai message. Il ignore le seuil et la désactivation automatique, mais respecte les exclusions, la position inconnue et la validité des données.
Il ne modifie pas la mémoire des alertes automatiques.

## Résultats

Réponse d’action facultative et événement vigilance_meteo_mobile_result : résultats par profil et destination.
Le capteur expose last_test_status et last_test_time, conservés en mémoire jusqu’au rechargement.

- test_envoye / envoye : appel de notification accepté, sans garantie de livraison ni lecture.
- position_inconnue : entité absente, unknown ou unavailable.
- departement_non_pris_en_charge : pays, attributs ou territoire non reconnus.
- departement_exclu : données éventuellement visibles, notification bloquée par le choix utilisateur.
- bulletin_perime / bulletin_invalide / departement_absent / api_indisponible : pas d’envoi à partir de données inutilisables.
- sous_le_seuil / automatique_desactive / deja_envoye : règle empêchant l’envoi automatique.
- resultat_partiel : destinations avec résultats différents ; lire le détail.
- action_notification_absente / erreur_notification : action introuvable ou erreur pendant l’appel.

## Doublons

Dernière signature par profil et destination, stockée localement. Inclut département, période, niveaux et créneaux, pas la seule heure de republication.
Une nouvelle journée ou un changement de département/niveaux/horaires peut notifier.
Ce n’est ni un historique illimité ni un rappel d’urgence. Les tags remplacent visuellement un message sans garantir l’absence de son/vibration.
La migration depuis les premières préversions peut provoquer un premier nouvel envoi du fait du format par destination.

## Limites

Métropole et Corse, zones départementales et bulletin d’aujourd’hui. Sous-zones littorales séparées et outre-mer non couverts.
Niveau maximal du bulletin, pas nécessairement actif maintenant ; des créneaux passés peuvent rester visibles.
Horaires selon Home Assistant. Dernière position remontée, sans contrôle de l’âge GPS réel.
Attributs pays/département attendus ; variantes non reconnues ignorées. Rendu de notification dépendant du téléphone.
Pas de plages silencieuses, d’annonce Google ni de confirmation de lecture dans cette version.

Les changements de configuration sont enregistrés seulement à la validation finale. Pas de confirmation de fermeture au clic extérieur ajoutée par l’intégration.
