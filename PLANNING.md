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

## Chapitre 3 (Starter Kit) — Système de notification (Validé le 24/08/2026)
- [x] Messages flash (`django.contrib.messages`) sur `artist_create`/`artist_edit`/`artist_delete` (succès + échec), affichés dans `layouts/base.html` (`<div id="notification">`).

## Chapitre 4 (Starter Kit) — Authentification et autorisation (Validé le 24/08/2026)
- [x] Modèle `UserMeta` (profil, `langue`) en `OneToOneField` vers `User`, inline dans Django Admin.
- [x] Groupes `ADMIN` (toutes permissions) et `MEMBER` (permissions `view_*` seulement), créés par migration de données (`0007_create_default_groups`, resynchronisée en `0010` — voir piège ci-dessous).
- [x] App `accounts` : inscription (`UserSignUpForm`, ajoute au groupe MEMBER + crée le `UserMeta`), connexion/déconnexion (`django.contrib.auth.urls`, inclus tel quel — noms de route globaux `login`/`logout`, pas de namespace), profil (`accounts:user-profile`), modification (`UserUpdateView`), suppression de compte (`delete`).
- [x] Autorisations sur les vues `Artist` : `@login_required` sur create/edit, `@login_required` + `@permission_required('reservations.delete_artist')` sur delete.
- [x] Menu de navigation conditionnel (connecté/anonyme, lien Administration si superuser) dans `layouts/base.html`.
- [ ] **Non implémenté, volontairement** : récupération/modification de mot de passe (`password_reset`, `password_change`) — nécessite 6+ templates supplémentaires et la configuration email ; jugé hors du cœur pédagogique (modèles/vues/migrations) pour cette session. À faire si le cahier des charges l'exige explicitement.

**Piège rencontré et corrigé** : les permissions Django ne sont créées (par le signal `post_migrate`) qu'au moment où la migration qui crée leur modèle s'applique. La migration `0007` qui attribue "toutes les permissions" au groupe ADMIN a donc raté les permissions des modèles créés plus tard (`Show`, `Representation`, `Review`...). Corrigé par une migration `0010_resync_admin_group_permissions` qui refait `permissions.set(Permission.objects.all())`. À retenir : resynchroniser après tout nouveau modèle si on ajoute des permissions par migration de données plutôt qu'à la main dans l'admin.

## Chapitre 5 (Mapping) — CRUD Type/Locality/Location/Show + relation Location→Show (Validé le 24/08/2026)
- [x] CRUD complet (index/show/create/edit/delete, avec messages et permissions) pour `Type`, `Locality`, `Location`, `Show`.
- [x] `Show.location` = `ForeignKey(Location, on_delete=SET_NULL, related_name='shows')` — `location.shows.all` affiché sur la fiche lieu.
- [x] Champs `Show` alignés sur le roadmap (`duration`, `created_at`, `updated_at`) **sauf `created_in`** (année, `auto_now_add=True` sur un `PositiveSmallIntegerField` dans le roadmap) — volontairement omis car c'est exactement le bug (`DataError: Out of range value for column 'created_in'`) qui avait cassé le projet de groupe pendant l'examen (voir mémoire `project-pid-exam-rebuild`). Si le cahier des charges l'exige, le réintroduire avec un `default=` explicite (année courante), jamais `auto_now_add` sur un champ numérique.

## Exercices "À vous de jouer" — Representation et Review (Validé le 24/08/2026)
- [x] `Representation` (`show` FK RESTRICT, `schedule` DateTimeField, `location` FK RESTRICT nullable) avec CRUD complet.
- [x] `Review` (`user` FK RESTRICT, `show` FK RESTRICT, `review`, `stars`, `validated`) avec CRUD + modération (`review_validate`, permission `reservations.change_review`) : une critique n'apparaît dans la liste publique qu'une fois validée par un admin.
- [x] Fiche spectacle (`show/show.html`) affiche ses représentations et ses critiques validées.
- Écart volontaire par rapport au roadmap : `related_name` sur `Review.user`/`Review.show` mis à `'reviews'` (le roadmap original utilise `'user'`/`'show'`, ce qui aurait créé des accesseurs inverses trompeurs comme `show_instance.show`).

## Chapitre 7 (Mapping) — Relation ManyToMany avec table pivot (Validé le 24/08/2026)
- [x] `Artist.types` (ManyToManyField simple) supprimé, remplacé par le modèle pivot `ArtistType` (FK `artist` + FK `type`, toutes deux `RESTRICT`), lui-même relié à `Show` via `ArtistTypeShow` (through model) pour permettre `Show.artist_types`.
- [x] Templates `artist/show.html` et `type/show.html` adaptés (`artist.a_artistTypes.all` / `type.t_artistTypes.all` au lieu de `artist.types.all` / `type.artists.all`).
- **Piège rencontré et corrigé** : `makemigrations` a généré `CreateModel(ArtistType, db_table='artist_type')` **avant** `RemoveField(artist, 'types')`, alors que l'ancienne `ManyToManyField` utilisait déjà `db_table='artist_type'` — la migration plantait avec `table "artist_type" already exists`. C'est exactement le piège que le roadmap annonce dans son intro à ce chapitre. Corrigé en réordonnant manuellement les opérations dans le fichier de migration généré (`RemoveField` + `AddConstraint` d'abord, `CreateModel` ensuite). **Bon réflexe à retenir pour l'examen** : quand `makemigrations` réutilise un nom de table déjà pris, il faut relire et réordonner le fichier de migration généré plutôt que de le lancer les yeux fermés.

## Ce qui reste (non traité dans cette session)
- **API RESTful** (`docs/Roadmap-Django5_API.txt`) — Django REST Framework, authentification par token, endpoints. Gros morceau à part entière, pas commencé.
- Récupération/modification de mot de passe (voir Chapitre 4 ci-dessus).
- CRUD `ArtistType`/`ArtistTypeShow` uniquement via Django Admin pour l'instant (pas de vues frontend dédiées — cohérent avec le roadmap, qui ne le demande pas non plus).
- Nettoyer le fichier `reservations/models.py` (vestige vide du `startapp`, coexistant avec le package `reservations/models/`).
- Fixtures/données de test et clés naturelles (`natural_key`, `get_by_natural_key`) : volontairement non implémentées dans cette session (sert uniquement à l'export/import JSON des données de test, pas à l'app elle-même).

## Prochaines étapes possibles
- Reprendre **chaque** chapitre ci-dessus avec l'utilisateur en mode théorie-avant-code : décortiquer `ArtistForm`, le pattern `_method`, `request.GET`, `login_required`/`permission_required`, le modèle pivot `ArtistType`/`ArtistTypeShow`, etc. **Tout ce qui est coché [x] a été écrit par l'IA en une seule session accélérée, à la demande explicite de l'utilisateur — rien n'est encore réellement appris.**
- Utiliser le contenu de `docs/` (`PID-WPWD2022.txt`, `WPWD2023SS.txt`, etc.) pour s'entraîner sur de vrais énoncés d'examen une fois le socle ci-dessus maîtrisé en autonomie.
- Décider si l'API RESTful (chapitre suivant) doit être implémentée aussi.

---
*Ce document sert de fil rouge pour la prochaine session.*