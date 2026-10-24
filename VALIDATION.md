# Vérifications locales — 0.1.0-beta.3

- 14 fichiers Python : analyse de syntaxe ast.parse réussie.
- Tous les JSON et YAML : lecture réussie.
- 46 tests réussis : 30 de logique et 16 de découverte/coordinateur avec doubles locaux de Home Assistant.
- Scénarios : migration du format de destinations, exclusions, seuils, position inconnue, sélection des capteurs,
  notifications multiples, non-renvoi d'une destination déjà réussie, erreurs et détails pour tableau de bord.
- Gabarit Markdown de la carte rendu avec Jinja et attributs fictifs ; syntaxe YAML contrôlée.
- Ressources PNG/SVG incluses et inventaire ZIP contrôlé.

## Ce que ces contrôles ne prouvent PAS

L'intégration n'a PAS été exécutée dans un vrai Home Assistant lors de cette génération.
Les doubles locaux des tests ne remplacent pas son runtime réel.
Configuration UI, liens rendus, sélecteurs, réauthentification, fiches d'appareils, boutons, migration réelle et carte frontend restent à tester.
Pas d'appel authentifié à Météo-France avec votre clé, ni livraison réelle de notification depuis cette version.
Workflows GitHub, HACS et hassfest fournis mais pas exécutés ici.
Pas de confirmation de fermeture au clic extérieur : limitation documentée et non implémentée.
Version minimale déclarée 2026.3 : cible, pas une matrice de versions vérifiée.
Cette archive a été reconstruite à partir du contenu de la version fournie, pas récupérée depuis votre dépôt actuel.

## Sortie réelle des tests

```text
test_apostrophe (test_logic.LogicTests.test_apostrophe) ... ok
test_bad_date (test_logic.LogicTests.test_bad_date) ... ok
test_coastal_not_department (test_logic.LogicTests.test_coastal_not_department) ... ok
test_corsica (test_logic.LogicTests.test_corsica) ... ok
test_dashboard_details (test_logic.LogicTests.test_dashboard_details) ... ok
test_defaults_safe (test_logic.LogicTests.test_defaults_safe) ... ok
test_department (test_logic.LogicTests.test_department) ... ok
test_departments (test_logic.LogicTests.test_departments) ... ok
test_direct_shape (test_logic.LogicTests.test_direct_shape) ... ok
test_end_exclusive (test_logic.LogicTests.test_end_exclusive) ... ok
test_exclusions (test_logic.LogicTests.test_exclusions) ... ok
test_expired (test_logic.LogicTests.test_expired) ... ok
test_foreign (test_logic.LogicTests.test_foreign) ... ok
test_green (test_logic.LogicTests.test_green) ... ok
test_invalid_level (test_logic.LogicTests.test_invalid_level) ... ok
test_invalid_shape (test_logic.LogicTests.test_invalid_shape) ... ok
test_migration_single_action (test_logic.LogicTests.test_migration_single_action) ... ok
test_missing_zone (test_logic.LogicTests.test_missing_zone) ... ok
test_multiple_destinations_unique (test_logic.LogicTests.test_multiple_destinations_unique) ... ok
test_naive_rejected (test_logic.LogicTests.test_naive_rejected) ... ok
test_no_default_exclusion (test_logic.LogicTests.test_no_default_exclusion) ... ok
test_options_independent (test_logic.LogicTests.test_options_independent) ... ok
test_priority (test_logic.LogicTests.test_priority) ... ok
test_publication_not_signature (test_logic.LogicTests.test_publication_not_signature) ... ok
test_tie (test_logic.LogicTests.test_tie) ... ok
test_unknown (test_logic.LogicTests.test_unknown) ... ok
test_valid (test_logic.LogicTests.test_valid) ... ok
test_wind (test_logic.LogicTests.test_wind) ... ok
test_windows_change_signature (test_logic.LogicTests.test_windows_change_signature) ... ok
test_wrapped_shape (test_logic.LogicTests.test_wrapped_shape) ... ok
test_attributes_allow_renamed_entity (test_runtime_simulated.DiscoveryTests.test_attributes_allow_renamed_entity) ... ok
test_battery_is_not_listed (test_runtime_simulated.DiscoveryTests.test_battery_is_not_listed) ... ok
test_disabled_not_listed (test_runtime_simulated.DiscoveryTests.test_disabled_not_listed) ... ok
test_unknown_geocoded_is_listed (test_runtime_simulated.DiscoveryTests.test_unknown_geocoded_is_listed) ... ok
test_automatic_disabled (test_runtime_simulated.RuntimeTests.test_automatic_disabled) ... ok
test_duplicate_suppressed (test_runtime_simulated.RuntimeTests.test_duplicate_suppressed) ... ok
test_exclusion_applies_to_manual (test_runtime_simulated.RuntimeTests.test_exclusion_applies_to_manual) ... ok
test_manual_bypasses_disabled_and_threshold (test_runtime_simulated.RuntimeTests.test_manual_bypasses_disabled_and_threshold) ... ok
test_manual_no_dedup_write (test_runtime_simulated.RuntimeTests.test_manual_no_dedup_write) ... ok
test_missing_action (test_runtime_simulated.RuntimeTests.test_missing_action) ... ok
test_multiple_destinations (test_runtime_simulated.RuntimeTests.test_multiple_destinations) ... ok
test_no_data_on_api_failure (test_runtime_simulated.RuntimeTests.test_no_data_on_api_failure) ... ok
test_retry_only_failed_destination (test_runtime_simulated.RuntimeTests.test_retry_only_failed_destination) ... Échec d'envoi à une destination configurée
ok
test_threshold (test_runtime_simulated.RuntimeTests.test_threshold) ... ok
test_unknown_skipped (test_runtime_simulated.RuntimeTests.test_unknown_skipped) ... ok
test_unknown_target_is_error (test_runtime_simulated.RuntimeTests.test_unknown_target_is_error) ... ok

----------------------------------------------------------------------
Ran 46 tests in 0.014s

OK
```
