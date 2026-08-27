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

## Exercice "à vous de jouer" — Reservation (Validé le 27/08/2026)
- [x] Modèle `Reservation` (`user` FK RESTRICT, `representation` FK RESTRICT, `quantity`, `price`, `created_at`) avec CRUD complet (`reservations/`, `reservation/create/`, `edit/`, `delete/`, `<id>/`), réservé aux utilisateurs connectés, chacun ne voit/modifie que ses propres réservations (même patron que `Review` : `get_object_or_404(Reservation, id=id, user=request.user)`).
- [x] `price` copié depuis `representation.show.price` au moment de la réservation (photo du prix, insensible à un changement ultérieur du prix du spectacle).
- **Écart volontaire par rapport au roadmap** : pas de modèle `Price` séparé ni de relation ManyToMany `Show↔Price`. `Show` a déjà un champ `price` simple, ajouté lors d'une session précédente ; dupliquer la notion avec un modèle Price contredirait la consigne de simplicité de l'utilisateur. `Reservation↔Representation` est implémenté en deux relations ManyToOne (vers `User` et `Representation`), exactement l'alternative que le roadmap propose lui-même à la relation ManyToMany avec table pivot enrichie.
- Lien "Mes réservations" dans la nav (visible si connecté), lien "Réserver" sur la fiche représentation.

## Chapitre 8 (API) — API RESTful avec Django REST Framework (Validé le 27/08/2026)
- [x] DRF déjà installé dans l'environnement (3.15.2, aucune installation nécessaire). Ajouté à `INSTALLED_APPS`.
- [x] API limitée au modèle `Artist` (comme le roadmap le fait lui-même) : `GET/POST /api/artists/`, `GET/PUT/DELETE /api/artists/<id>/`.
- [x] `ArtistSerializer` avec champ `links` (HATEOAS, `self` + `all_artists`), comme le roadmap le demande.
- [x] Authentification Session + Basic (`REST_FRAMEWORK` dans `settings.py`). Permission `DjangoModelPermissionsOrAnonReadOnly` : lecture publique (cohérent avec le reste du site), écriture soumise aux permissions Django existantes (groupes ADMIN/MEMBER déjà créés au chapitre 4) — aucun système de permission séparé à maintenir.
- Testé avec `curl -u admin:... / -u bob:...` : lecture publique OK, écriture anonyme 403, écriture par `bob` (MEMBER, pas de `add_artist`) 403, écriture par `admin` 201/204.
- **Non fait, volontairement** : authentification JWT (`§8.4` du roadmap, explicitement "optionnel", nécessite une dépendance `djangorestframework-simplejwt` non installée), tests automatisés DRF (`§11`, "optionnel"), documentation Swagger (`§13`, marqué TODO dans le roadmap lui-même), API pour les autres modèles (hors du scope du roadmap, qui ne couvre qu'Artist).

## Chapitre 4 (suite) — Mot de passe oublié / changement (Validé le 27/08/2026)
- [x] Les routes existaient déjà (`django.contrib.auth.urls` inclus dans `projet_reservation/urls.py`) et `EMAIL_BACKEND` était déjà en mode console — il ne manquait que les 7 templates (`accounts/templates/registration/password_reset_*.html`, `password_change_*.html`), écrits dans le même style minimal que `login.html`.
- **Piège rencontré et corrigé** : `django.contrib.admin` embarque ses propres templates `registration/password_reset_*.html` (stylés en CSS admin). Comme il était listé avant `reservations`/`accounts` dans `INSTALLED_APPS`, le chargeur de templates (`APP_DIRS`, qui cherche dans l'ordre des apps installées) trouvait la version admin avant la nôtre. Corrigé en plaçant `reservations` et `accounts` en tête de `INSTALLED_APPS`. À retenir : quand un template `registration/*` semble "ignorer" nos modifications, vérifier l'ordre de `INSTALLED_APPS` avant de chercher ailleurs.
- Testé de bout en bout : demande de réinitialisation → email affiché dans le terminal (backend console) → lien de réinitialisation fonctionnel → nouveau mot de passe pris en compte.

## Nettoyage et données de test (27/08/2026)
- [x] Suppression du fichier vestige `reservations/models.py` (coexistait avec le package `reservations/models/`, jamais utilisé).
- [x] Identifiants de test créés (mot de passe de `admin` réinitialisé, utilisateur `bob` créé dans le groupe MEMBER) — voir `CREDENTIALS.txt` à la racine (non commité, dans `.gitignore`).
- [x] Données de démonstration ajoutées (1 localité, 1 lieu, 2 spectacles avec prix, 2 représentations) pour pouvoir tester réellement l'application (la base ne contenait avant que les artistes/types).
- [x] **Bug corrigé** : les vues `index`, `contact` et `about` (`reservations/views.py`) étaient encore de vieux vestiges du chapitre 1 (routage niveau 1) — un `HttpResponse` codé en dur, sans passer par `layouts/base.html`. Conséquence : le menu de connexion/navigation n'apparaissait pas sur ces 3 pages, contrairement à toutes les autres. Corrigé en les convertissant en `render()` avec des templates minimalistes (`templates/index.html`, `contact.html`, `about.html`, chacun `extends 'layouts/base.html'`).

## Formulaires : séparation des champs (27/08/2026)
- [x] Tous les formulaires (`{{ form }}` brut, sans structure) remplacés par `<table>{{ form.as_table }}</table>` — un champ par ligne, toujours zéro CSS, même principe que les formulaires de mot de passe déjà écrits ainsi. 18 templates concernés (CRUD Artist/Type/Locality/Location/Show/Representation/Review/Reservation, inscription, modification de profil).

## Dashboard admin (27/08/2026)
- [x] Nouvelle page `reservations:dashboard` (`/dashboard/`), réservée aux membres du groupe ADMIN ou superuser (`user_passes_test(is_admin)`, `is_admin` défini dans `reservations/views.py`) : compteurs de tout le catalogue (artistes, types, localités, lieux, spectacles, représentations, réservations, critiques dont en attente, membres), liens rapides vers la gestion de chaque contenu, et liste des critiques en attente de modération avec bouton « Valider » direct (réutilise `review_validate`).
- Lien « Tableau de bord » ajouté dans la nav (`layouts/base.html`), visible via `perms.reservations.add_show` (permission que seul le groupe ADMIN possède, MEMBER n'a que des `view_*`) ou `is_superuser` — même logique que le lien Administration existant vers `/admin/`.

## Balayage complet du cahier des charges (PID) (27/08/2026)
À la demande explicite de l'utilisateur ("tout"), quasiment toutes les fonctionnalités fonctionnelles du PID encore manquantes ont été implémentées en une série de commits, chacun documenté en détail dans son message de commit (`git log`) :
- **Rôle producteur** : `Show.producer` (FK User), groupe `PRODUCER`, espace `/producteur/` (statistiques de vente par spectacle — places réservées, recette —, modération des critiques et articles de presse limitée aux spectacles produits par l'utilisateur connecté).
- **Rôle critique de presse** : modèle `PressArticle`, groupe `CRITIC`, CRUD (soumission, modification avant publication, suppression), publication réservée au producteur du spectacle concerné ou à un admin. Articles publiés affichés sur la fiche spectacle.
- **API affiliés à paliers** : `UserMeta.affiliate_tier` (none/free/starter/premium), `AffiliateTierThrottle` (`reservations/throttling.py`) limite les requêtes/jour selon le palier (Free 20/j, Starter 200/j, Premium 2000/j). API Show en lecture seule ajoutée en plus d'Artist. Le palier se configure via Django Admin (pas de flux d'upgrade dédié).
- **Flux RSS** : `/rss/representations/`, les 20 prochaines représentations, via `django.contrib.syndication` (le « progiciel » demandé par l'itération 7).
- **Export/import CSV** du catalogue de spectacles depuis le dashboard admin.
- **Intégration web service tiers** : `reservations/webservice.py` + commande `sync_shows_from_webservice` + bouton dashboard. Structure prête et testée (gestion d'erreurs réseau/format), mais `settings.THIRD_PARTY_CATALOG_API_URL` est vide par défaut — **aucun fournisseur réel n'est branché**, le PID n'en nomme pas pour cette fonctionnalité précise (contrairement à l'itération 9, qui liste des API nécessitant chacune la création d'un compte par l'utilisateur).
- **Catalogue des spectacles** : pagination (10/page), tri (titre/lieu/réservable/prix), filtres (lieu, réservable), recherche par titre — reprend le use case « Consulter le catalogue paginé des spectacles » du PID.
- **Bandeau cookies** (`/cookies/accepter/`), sans JS, cohérent avec le reste du site.
- **Règles métier inscription** : mot de passe ≥ 6 caractères + 1 majuscule + 1 caractère spécial (`accounts/validators.py`, `AUTH_PASSWORD_VALIDATORS`), email unique (`UserSignUpForm.clean_email`).
- **Espace personnel** (page profil) : résumé des réservations/achats (nombre, places, montant total dépensé), critiques postées, articles de presse soumis, avec liens vers les listes complètes.

### Décisions explicites de ne PAS implémenter (documentées, pas oubliées)
- **Frontend JS (React/Angular/Vue/AJAX)** : le PID le recommande (itération 8) mais **contredit directement** la préférence forte et répétée de l'utilisateur pour du HTML minimal sans style ni JS (voir [[feedback-django-minimal-html]]). Ce conflit est tranché en faveur de la préférence explicite de l'utilisateur.
- **Itération 9 (consommer une vraie API RESTful externe)** : toutes les API suggérées (London Theater, Théâtre de la ville de Paris, Agenda.Brussels...) nécessitent la création d'un compte / une clé API par l'utilisateur — impossible à faire de façon autonome sans ses identifiants.
- **Authentification API par JWT, tests automatisés DRF, documentation Swagger** : toujours marqués optionnels/TODO dans le roadmap Django lui-même (pas le PID).
- **Actions groupées sur le catalogue** ("sélectionner des éléments et effectuer des actions groupées") : déjà couvert par Django Admin (actions en masse natives sur tous les modèles enregistrés) — pas de réimplémentation frontend.
- **Diagrammes (contexte, cas d'utilisation, classes participantes), business model, étude comparative** : ce sont des livrables de rapport/analyse (UML, texte), pas du code — hors du périmètre d'un agent de développement.
- CRUD `ArtistType`/`ArtistTypeShow` en frontend dédié, fixtures/clés naturelles, modèle `Price` séparé : toujours hors scope, voir raisons documentées plus haut dans ce fichier.

## Prochaines étapes possibles
- Reprendre **chaque** fonctionnalité de ce document avec l'utilisateur en mode théorie-avant-code : rien de ce qui est coché [x] n'a été expliqué ligne par ligne, tout a été écrit en session accélérée à la demande explicite de l'utilisateur.
- Utiliser le contenu de `docs/example d examen/` pour s'entraîner sur de vrais énoncés d'examen une fois le socle ci-dessus maîtrisé en autonomie.
- Si un vrai fournisseur de web service ou d'API affiliés doit être branché, il faudra que l'utilisateur fournisse l'URL/les identifiants — `settings.THIRD_PARTY_CATALOG_API_URL` est le point d'entrée pour le premier cas.

---
*Ce document sert de fil rouge pour la prochaine session.*