# Obtenir et protéger la clé Météo-France

## Accès

1. Ouvrir le portail officiel https://portail-api.meteofrance.fr/ (également accessible depuis https://donneespubliques.meteofrance.fr/).
2. Créer un compte ou se connecter et valider le compte si demandé.
3. Dans le catalogue, rechercher l'API Vigilance / Données publiques Vigilance correspondant à `DPVigilance`.
4. Lire les conditions d'utilisation et souscrire/activer l'accès à cette API selon la procédure du portail.
5. Dans l'espace de gestion de cette API, générer une clé de type API Key autorisée à l'utiliser.
6. Noter les quotas et la durée de validité. Les libellés du portail peuvent évoluer : sa documentation prévaut.
7. Coller uniquement la valeur de la clé dans le champ de l'intégration.

Créer un compte ne suffit pas forcément : la clé et l'autorisation doivent couvrir la bonne API.
La bêta utilise une API Key passée dans `apikey`, pas un jeton OAuth Bearer.

## Requête effectuée

```text
GET https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours
accept: application/json
apikey: VOTRE_CLE
```

Timeout : 30 secondes. Bulletin national : la position de votre téléphone n'est pas placée dans la requête.
Un téléchargement par actualisation pour tous les destinataires de l'intégration.

## Quotas et erreurs

- 401/403 : vérifier la clé, sa validité, le type d'authentification et la souscription API.
- 429 : quota/fréquence excessive ; augmenter l'intervalle, tenir compte des scripts ou autres clients utilisant la même clé.
- 5xx/timeout : réessayer plus tard. Aucune notification n'est envoyée à partir d'une récupération échouée.
- Une réponse 200 dont la structure est incorrecte n'est pas interprétée comme un bulletin vert.
- Ne pas lancer de tests en boucle : ils peuvent demander une actualisation réseau.

## Modifier la clé

Depuis l'entrée de l'intégration, utiliser Reconfigurer pour saisir une nouvelle clé.
Si Home Assistant propose une réparation/réauthentification après refus API, suivre ce formulaire.
Un rechargement de l'intégration est effectué après changement.

## Sécurité

Ne pas coller une clé dans GitHub, README, capture, ticket, automation publique ou chat public.
La clé est stockée dans la configuration locale de Home Assistant, sans chiffrement supplémentaire par cette intégration.
Les sauvegardes peuvent la contenir : les protéger. Révoquer une clé exposée puis la remplacer.

Un ancien `rest_command` avec `!secret` reste indépendant. Cette intégration ne lit pas automatiquement secrets.yaml.
Il n'est pas nécessaire d'ajouter rest_command pour l'utiliser.
