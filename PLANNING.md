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

## Prochaines Étapes : Maîtriser le Routage (URLs) et les Vues

Nous allons aborder la partie Frontend en suivant ce plan progressif strict :

### Niveau 1 : L'URL statique et simple (Niveau Racine)
- Création d'une page d'accueil basique (`path('', ...)`).
- Comprendre comment la requête arrive dans une vue et renvoie un texte ou un template simple.

### Niveau 2 : La délégation (Include)
- Comprendre pourquoi et comment on sépare le fichier `urls.py` du projet du fichier `urls.py` de l'application `reservations`.
- Créer une route statique dans l'application (ex: `/artistes/`).

### Niveau 3 : L'URL dynamique (L'Identifiant)
- Passer un paramètre technique simple dans l'URL.
- Exemple : Afficher le détail d'un seul artiste via son ID/PK (`/artiste/<int:id>/`).
- Comment la Vue récupère cet ID pour interroger la base de données.

### Niveau 4 : Les URLs CRUD (Conventions)
- Structurer les URLs selon les bonnes pratiques pour les opérations CRUD.
- Exemple : `/artiste/create/`, `/artiste/edit/<int:id>/`, `/artiste/delete/<int:id>/`.

### Niveau 5 : L'URL paramétrée complexe (Mots et SEO)
- Passer des chaînes de caractères (strings) dans l'URL (comme l'examen 2022).
- Exemple : Filtrer les spectacles par nom de salle (`/salle/<str:room_name>/`).

### Niveau 6 : L'URL de Recherche (Query String)
- La différence fondamentale avec les paramètres de route.
- Comprendre l'usage du `?` dans l'URL pour les formulaires de recherche (`/spectacles/?q=theatre`).
- Comment lire ces données dans la Vue (`request.GET`).

---
*Ce document sert de fil rouge pour la prochaine session.*