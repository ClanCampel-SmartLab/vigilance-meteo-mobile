# Obtenir une clé API Météo-France

## Portail et accès

1. Ouvrir https://portail-api.meteofrance.fr/ depuis le lien dans le formulaire.
2. Créer un compte ou se connecter ; terminer la validation du compte si demandée.
3. Dans le catalogue, rechercher l'API Vigilance / Données publiques Vigilance correspondant à DPVigilance.
4. Lire les conditions d'utilisation et activer/souscrire à cette API selon la procédure du portail.
5. Générer une API Key autorisée pour cet accès ; relever durée de validité et quotas.
6. Coller sa VALEUR dans le champ de l'intégration, sans `!secret` et sans publier la clé.

Les libellés du portail peuvent évoluer. Un compte seul ne suffit pas forcément : la clé doit avoir accès à la bonne API.
Le lien vers les données publiques officielles est https://donneespubliques.meteofrance.fr/.
Cette version ne traite pas un jeton OAuth Bearer à la place d'une API Key.

## Requête

```text
GET https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours
accept: application/json
apikey: VOTRE_CLE
```

Timeout 30 secondes. Un bulletin national est partagé entre les profils. La position du téléphone n'est pas envoyée à cette URL.

## Erreurs

- 401/403 : vérifier clé, autorisation, validité et souscription.
- 429 : quota ; augmenter l'intervalle et tenir compte des autres scripts utilisant la même clé.
- 5xx/timeout : réessayer ultérieurement. Aucun faux bulletin vert n'est créé.
- 200 avec contenu non reconnu : réponse rejetée.

Éviter les tests répétés en boucle : ils peuvent demander une actualisation réseau.
Changer la clé depuis Reconfigurer sur l'entrée ou suivre la réauthentification proposée par Home Assistant.

## Stockage

La clé est enregistrée dans la configuration interne de Home Assistant, sans chiffrement supplémentaire par cette intégration.
Protéger sauvegardes et accès. Ne pas publier .storage, secrets.yaml ou captures contenant la clé.
Révoquer une clé exposée avant de la remplacer.
Ni configuration.yaml ni secrets.yaml ne sont modifiés. Aucun rest_command n'est nécessaire.
