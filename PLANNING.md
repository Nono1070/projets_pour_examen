# Plan d'Apprentissage et Suivi du Projet Réservations

## État d'avancement
- **Environnement** : Projet Django créé et configuré.
- **Itération 1 (Validée)** : Serveur fonctionnel, application `reservations` enregistrée.
- **Itérations 2 & 3 (Modèles de base)** : Modèles créés sans relations complexes (clés étrangères volontairement omises pour l'instant).
  - [x] Artist
  - [x] Type
  - [x] Locality
  - [x] Location
  - [x] Show
- **Migrations** : Comprises et appliquées avec succès. (Notion de "nettoyage" en cas de blocage d'examen acquise).
- **Administration** : Back-office configuré, modèles enregistrés et personnalisés.

## Méthodologie Pédagogique (À respecter par l'IA)
L'utilisateur souhaite une approche **progressive (crescendo)** et **théorique avant la pratique**.

**Règles pour la suite des explications :**
1. **Théorie d'abord** : Pas de code (ou seulement des exemples génériques) tant que le concept n'est pas compris.
2. **Décortiquer** : Expliquer chaque ligne, chaque mot-clé (ce qui vient du framework vs ce qui est choisi par l'utilisateur).
3. **Progression stricte (Pas à pas)** : Ne pas introduire de concepts avancés (comme les clés étrangères ou les query strings) avant que les bases ne soient parfaitement assimilées.

---

## Routage (URLs) et Vues — Niveaux 1 à 6 (Validés le 24/08/2026)

Toute la progression a été implémentée d'un coup par l'IA (à la demande explicite de l'utilisateur, qui teste en parallèle l'auto-complétion Copilot/VSCode) sur le modèle `Artist`, avec un commit git séparé et testé à chaque niveau. **Le mode théorie-avant-code n'a donc pas été respecté pour cette session** — à relire/expliquer ligne par ligne avec l'utilisateur avant de considérer ces niveaux réellement acquis.

- [x] **Niveau 1** : URL racine statique (`/`).
- [x] **Niveau 2** : Délégation via `include('reservations.urls')` depuis `projet_reservation/urls.py`.
- [x] **Niveau 3** : URL dynamique `artist/<int:id>/` → `show_artist`.
- [x] **Niveau 4** : CRUD complet pour `Artist` — `ArtistForm` (ModelForm), templates (`layouts/base.html`, `artist/index.html`, `show.html`, `create.html`, `edit.html`), vues `artist_index`, `show_artist`, `artist_create`, `artist_edit`, `artist_delete`. Convention `_method` (PUT/DELETE) en champ caché de formulaire, comme dans le roadmap officiel.
- [x] **Niveau 5** : URL avec paramètre string — `artistes/type/<str:type_name>/` → `artist_by_type`, filtre les artistes par type via la relation ManyToMany déjà en place.
- [x] **Niveau 6** : Recherche par query string — `artistes/?q=...` filtre `artist_index` sur `lastname__icontains`.

Historique des commits (voir `git log`) :
1. `Mise en place du projet Django, modeles de base (...) et routes niveau 1 a 3` — rattrapage du travail déjà fait mais jamais committé.
2. `Vue Artist en templates (index et show) + layout de base`
3. `Formulaire ArtistForm et vue de creation d'un artiste`
4. `Vue de modification (edit) d'un artiste`
5. `Vue de suppression (delete) d'un artiste`
6. `Niveau 5 : filtre des artistes par type via parametre string dans l'URL`
7. `Niveau 6 : recherche des artistes par nom via query string (?q=)`

Environnement d'exécution : `..\python-3.12.0-embed-amd64\python.exe manage.py runserver` (Python embarqué sur la clé USB, voir `lancement_django.bat` à la racine de la clé) — pas de venv dans ce dossier.

## Prochaines étapes possibles
- Reprendre chaque niveau avec l'utilisateur en mode théorie-avant-code (décortiquer `ArtistForm`, le pattern `_method`, `request.GET`, etc.) pour combler l'écart créé par cette session accélérée.
- Étendre le même pattern CRUD aux autres modèles (`Type`, `Locality`, `Location`, `Show`) si voulu.
- Nettoyer le fichier `reservations/models.py` (vestige vide du `startapp`, coexistant avec le package `reservations/models/`).
- Utiliser le contenu de `docs/` (`PID-WPWD2022.txt`, `WPWD2023SS.txt`, etc.) pour s'entraîner sur de vrais énoncés d'examen une fois les niveaux 1 à 6 maîtrisés en autonomie.

---
*Ce document sert de fil rouge pour la prochaine session.*