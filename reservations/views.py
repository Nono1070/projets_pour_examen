import csv
import io

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Sum, F
from django.utils import timezone

from .models import Artist, Type, Locality, Location, Show, Representation, Review, Reservation, PressArticle, RoleRequest
from .forms import ArtistForm, TypeForm, LocalityForm, LocationForm, ShowForm, RepresentationForm, ReviewForm, ReservationForm, PressArticleForm
from .webservice import sync_shows_from_webservice, WebserviceSyncError


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='ADMIN').exists()


def is_producer(user):
    return user.groups.filter(name='PRODUCER').exists()


COOKIE_CONSENT_NAME = 'cookie_consent'
COOKIE_CONSENT_MAX_AGE = 60 * 60 * 24 * 365


def accept_cookies(request):
    if request.method == 'POST':
        redirect_to = request.POST.get('next') or 'reservations:index'
        response = redirect(redirect_to)
        response.set_cookie(COOKIE_CONSENT_NAME, '1', max_age=COOKIE_CONSENT_MAX_AGE)

        return response

    return redirect('reservations:index')


def _shows_catalog_context(request):
    """
    Contexte partage par la page d'accueil et le catalogue des spectacles
    (/spectacles/) : recherche par titre, filtres (lieu, reservable), tri
    et pagination, plus la prochaine representation a venir de chaque
    spectacle affiche (PID : "affichant le lieu et les prochaines dates
    de representation").
    """
    shows = Show.objects.all()
    title = 'Liste des spectacles'

    query = request.GET.get('q')
    if query:
        shows = shows.filter(title__icontains=query)
        title = f"Résultats pour « {query} »"

    location_id = request.GET.get('location')
    if location_id:
        shows = shows.filter(location_id=location_id)

    bookable = request.GET.get('bookable')
    if bookable in ('1', '0'):
        shows = shows.filter(bookable=(bookable == '1'))

    sort_fields = {
        'title': 'title',
        'location': 'location__designation',
        'bookable': 'bookable',
        'price': 'price',
    }
    sort = request.GET.get('sort', 'title')
    shows = shows.order_by(sort_fields.get(sort, 'title'))

    paginator = Paginator(shows, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    shows_with_next = [
        {
            'show': show,
            'next_representation': show.representations.filter(schedule__gte=timezone.now()).order_by('schedule').first(),
        }
        for show in page_obj
    ]

    return {
        'shows': page_obj,
        'shows_with_next': shows_with_next,
        'title': title,
        'query': query or '',
        'locations': Location.objects.all(),
        'selected_location': location_id or '',
        'selected_bookable': bookable or '',
        'sort': sort,
    }


# Create your views here.
def index(request):
    return render(request, 'index.html', _shows_catalog_context(request))


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def artist_index(request):
    artists = Artist.objects.all()
    title = 'Liste des artistes'

    query = request.GET.get('q')
    if query:
        artists = artists.filter(lastname__icontains=query)
        title = f"Résultats pour « {query} »"

    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': title,
        'query': query or '',
    })


def show_artist(request, id):
    artist = get_object_or_404(Artist, id=id)

    return render(request, 'artist/show.html', {
        'artist': artist,
    })


@login_required
@permission_required('reservations.add_artist', raise_exception=True)
def artist_create(request):
    form = ArtistForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouvel artiste créé avec succès.")

            return redirect('reservations:artist_index')
        else:
            messages.error(request, "Échec de l'ajout d'un nouvel artiste !")

    return render(request, 'artist/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_artist', raise_exception=True)
def artist_edit(request, id):
    # on récupère l'objet correspondant à l'id passé dans l'URL
    artist = get_object_or_404(Artist, id=id)

    # on passe l'objet en instance dans le formulaire
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Artiste modifié avec succès.")

                return redirect('reservations:show_artist', id=artist.id)
            else:
                messages.error(request, "Échec de la modification de l'artiste !")

    return render(request, 'artist/edit.html', {
        'form': form,
        'artist': artist,
    })


@login_required
@permission_required('reservations.delete_artist', raise_exception=True)
def artist_delete(request, id):
    artist = get_object_or_404(Artist, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            artist.delete()
            messages.success(request, "Artiste supprimé avec succès.")

            return redirect('reservations:artist_index')
        else:
            messages.error(request, "Échec de la suppression de l'artiste !")

    return render(request, 'artist/show.html', {
        'artist': artist,
    })


def artist_by_type(request, type_name):
    artists = Artist.objects.filter(a_artistTypes__type__type__iexact=type_name)
    title = f"Artistes de type : {type_name}"

    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': title,
        'query': '',
    })


# --- Type ---

def type_index(request):
    types = Type.objects.all()

    return render(request, 'type/index.html', {
        'types': types,
        'title': 'Liste des types',
    })


def show_type(request, id):
    type_ = get_object_or_404(Type, id=id)

    return render(request, 'type/show.html', {
        'type': type_,
    })


@login_required
@permission_required('reservations.add_type', raise_exception=True)
def type_create(request):
    form = TypeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouveau type créé avec succès.")

            return redirect('reservations:type_index')
        else:
            messages.error(request, "Échec de l'ajout d'un nouveau type !")

    return render(request, 'type/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_type', raise_exception=True)
def type_edit(request, id):
    type_ = get_object_or_404(Type, id=id)
    form = TypeForm(request.POST or None, instance=type_)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Type modifié avec succès.")

                return redirect('reservations:show_type', id=type_.id)
            else:
                messages.error(request, "Échec de la modification du type !")

    return render(request, 'type/edit.html', {
        'form': form,
        'type': type_,
    })


@login_required
@permission_required('reservations.delete_type', raise_exception=True)
def type_delete(request, id):
    type_ = get_object_or_404(Type, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            type_.delete()
            messages.success(request, "Type supprimé avec succès.")

            return redirect('reservations:type_index')
        else:
            messages.error(request, "Échec de la suppression du type !")

    return render(request, 'type/show.html', {
        'type': type_,
    })


# --- Locality ---

def locality_index(request):
    localities = Locality.objects.all()

    return render(request, 'locality/index.html', {
        'localities': localities,
        'title': 'Liste des localités',
    })


def show_locality(request, id):
    locality = get_object_or_404(Locality, id=id)

    return render(request, 'locality/show.html', {
        'locality': locality,
    })


@login_required
@permission_required('reservations.add_locality', raise_exception=True)
def locality_create(request):
    form = LocalityForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouvelle localité créée avec succès.")

            return redirect('reservations:locality_index')
        else:
            messages.error(request, "Échec de l'ajout d'une nouvelle localité !")

    return render(request, 'locality/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_locality', raise_exception=True)
def locality_edit(request, id):
    locality = get_object_or_404(Locality, id=id)
    form = LocalityForm(request.POST or None, instance=locality)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Localité modifiée avec succès.")

                return redirect('reservations:show_locality', id=locality.id)
            else:
                messages.error(request, "Échec de la modification de la localité !")

    return render(request, 'locality/edit.html', {
        'form': form,
        'locality': locality,
    })


@login_required
@permission_required('reservations.delete_locality', raise_exception=True)
def locality_delete(request, id):
    locality = get_object_or_404(Locality, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            locality.delete()
            messages.success(request, "Localité supprimée avec succès.")

            return redirect('reservations:locality_index')
        else:
            messages.error(request, "Échec de la suppression de la localité !")

    return render(request, 'locality/show.html', {
        'locality': locality,
    })


# --- Location ---

def location_index(request):
    locations = Location.objects.all()

    return render(request, 'location/index.html', {
        'locations': locations,
        'title': 'Liste des lieux',
    })


def show_location(request, id):
    location = get_object_or_404(Location, id=id)

    return render(request, 'location/show.html', {
        'location': location,
    })


@login_required
@permission_required('reservations.add_location', raise_exception=True)
def location_create(request):
    form = LocationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouveau lieu créé avec succès.")

            return redirect('reservations:location_index')
        else:
            messages.error(request, "Échec de l'ajout d'un nouveau lieu !")

    return render(request, 'location/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_location', raise_exception=True)
def location_edit(request, id):
    location = get_object_or_404(Location, id=id)
    form = LocationForm(request.POST or None, instance=location)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Lieu modifié avec succès.")

                return redirect('reservations:show_location', id=location.id)
            else:
                messages.error(request, "Échec de la modification du lieu !")

    return render(request, 'location/edit.html', {
        'form': form,
        'location': location,
    })


@login_required
@permission_required('reservations.delete_location', raise_exception=True)
def location_delete(request, id):
    location = get_object_or_404(Location, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            location.delete()
            messages.success(request, "Lieu supprimé avec succès.")

            return redirect('reservations:location_index')
        else:
            messages.error(request, "Échec de la suppression du lieu !")

    return render(request, 'location/show.html', {
        'location': location,
    })


# --- Show ---

def show_index(request):
    return render(request, 'show/index.html', _shows_catalog_context(request))


def show_show(request, id):
    show = get_object_or_404(Show, id=id)

    return render(request, 'show/show.html', {
        'show': show,
    })


@login_required
@permission_required('reservations.add_show', raise_exception=True)
def show_create(request):
    form = ShowForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouveau spectacle créé avec succès.")

            return redirect('reservations:show_index')
        else:
            messages.error(request, "Échec de l'ajout d'un nouveau spectacle !")

    return render(request, 'show/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_show', raise_exception=True)
def show_edit(request, id):
    show = get_object_or_404(Show, id=id)
    form = ShowForm(request.POST or None, instance=show)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Spectacle modifié avec succès.")

                return redirect('reservations:show_show', id=show.id)
            else:
                messages.error(request, "Échec de la modification du spectacle !")

    return render(request, 'show/edit.html', {
        'form': form,
        'show': show,
    })


@login_required
@permission_required('reservations.delete_show', raise_exception=True)
def show_delete(request, id):
    show = get_object_or_404(Show, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            show.delete()
            messages.success(request, "Spectacle supprimé avec succès.")

            return redirect('reservations:show_index')
        else:
            messages.error(request, "Échec de la suppression du spectacle !")

    return render(request, 'show/show.html', {
        'show': show,
    })


# --- Representation ---

def representation_index(request):
    representations = Representation.objects.all()

    return render(request, 'representation/index.html', {
        'representations': representations,
        'title': 'Liste des représentations',
    })


def show_representation(request, id):
    representation = get_object_or_404(Representation, id=id)

    return render(request, 'representation/show.html', {
        'representation': representation,
    })


@login_required
@permission_required('reservations.add_representation', raise_exception=True)
def representation_create(request):
    form = RepresentationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Nouvelle représentation créée avec succès.")

            return redirect('reservations:representation_index')
        else:
            messages.error(request, "Échec de l'ajout d'une nouvelle représentation !")

    return render(request, 'representation/create.html', {
        'form': form,
    })


@login_required
@permission_required('reservations.change_representation', raise_exception=True)
def representation_edit(request, id):
    representation = get_object_or_404(Representation, id=id)
    form = RepresentationForm(request.POST or None, instance=representation)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Représentation modifiée avec succès.")

                return redirect('reservations:show_representation', id=representation.id)
            else:
                messages.error(request, "Échec de la modification de la représentation !")

    return render(request, 'representation/edit.html', {
        'form': form,
        'representation': representation,
    })


@login_required
@permission_required('reservations.delete_representation', raise_exception=True)
def representation_delete(request, id):
    representation = get_object_or_404(Representation, id=id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            representation.delete()
            messages.success(request, "Représentation supprimée avec succès.")

            return redirect('reservations:representation_index')
        else:
            messages.error(request, "Échec de la suppression de la représentation !")

    return render(request, 'representation/show.html', {
        'representation': representation,
    })


# --- Review ---

def review_index(request):
    reviews = Review.objects.filter(validated=True)

    return render(request, 'review/index.html', {
        'reviews': reviews,
        'title': 'Liste des critiques',
    })


def show_review(request, id):
    review = get_object_or_404(Review, id=id)

    return render(request, 'review/show.html', {
        'review': review,
    })


@login_required
def review_create(request):
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.validated = False
            review.save()
            messages.success(request, "Critique envoyée avec succès, en attente de modération.")

            return redirect('reservations:review_index')
        else:
            messages.error(request, "Échec de l'ajout de la critique !")

    return render(request, 'review/create.html', {
        'form': form,
    })


@login_required
def review_edit(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                review = form.save(commit=False)
                review.validated = False
                review.save()
                messages.success(request, "Critique modifiée avec succès, en attente de nouvelle modération.")

                return redirect('reservations:show_review', id=review.id)
            else:
                messages.error(request, "Échec de la modification de la critique !")

    return render(request, 'review/edit.html', {
        'form': form,
        'review': review,
    })


@login_required
def review_delete(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            review.delete()
            messages.success(request, "Critique supprimée avec succès.")

            return redirect('reservations:review_index')
        else:
            messages.error(request, "Échec de la suppression de la critique !")

    return render(request, 'review/show.html', {
        'review': review,
    })


@login_required
@permission_required('reservations.change_review', raise_exception=True)
def review_validate(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        review.validated = True
        review.save()
        messages.success(request, "Critique validée avec succès.")

    return redirect('reservations:show_review', id=review.id)


# --- Reservation ---

@login_required
def reservation_index(request):
    reservations = Reservation.objects.filter(user=request.user)

    return render(request, 'reservation/index.html', {
        'reservations': reservations,
        'title': 'Mes réservations',
    })


@login_required
def show_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id, user=request.user)

    return render(request, 'reservation/show.html', {
        'reservation': reservation,
    })


@login_required
def reservation_create(request):
    form = ReservationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.price = reservation.representation.show.price
            reservation.save()
            messages.success(request, "Réservation effectuée avec succès.")

            return redirect('reservations:reservation_index')
        else:
            messages.error(request, "Échec de la réservation !")

    return render(request, 'reservation/create.html', {
        'form': form,
    })


@login_required
def reservation_edit(request, id):
    reservation = get_object_or_404(Reservation, id=id, user=request.user)
    form = ReservationForm(request.POST or None, instance=reservation)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.price = reservation.representation.show.price
                reservation.save()
                messages.success(request, "Réservation modifiée avec succès.")

                return redirect('reservations:show_reservation', id=reservation.id)
            else:
                messages.error(request, "Échec de la modification de la réservation !")

    return render(request, 'reservation/edit.html', {
        'form': form,
        'reservation': reservation,
    })


@login_required
def reservation_delete(request, id):
    reservation = get_object_or_404(Reservation, id=id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            reservation.delete()
            messages.success(request, "Réservation annulée avec succès.")

            return redirect('reservations:reservation_index')
        else:
            messages.error(request, "Échec de l'annulation de la réservation !")

    return render(request, 'reservation/show.html', {
        'reservation': reservation,
    })


# --- Dashboard admin ---

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'dashboard.html', {
        'counts': {
            'artists': Artist.objects.count(),
            'types': Type.objects.count(),
            'localities': Locality.objects.count(),
            'locations': Location.objects.count(),
            'shows': Show.objects.count(),
            'representations': Representation.objects.count(),
            'reservations': Reservation.objects.count(),
            'reviews': Review.objects.count(),
            'reviews_pending': Review.objects.filter(validated=False).count(),
            'members': User.objects.count(),
        },
        'pending_reviews': Review.objects.filter(validated=False).order_by('-created_at')[:10],
        'pending_role_requests': RoleRequest.objects.filter(status=RoleRequest.Status.PENDING),
    })


@login_required
@user_passes_test(is_admin)
def export_shows_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="spectacles.csv"'

    writer = csv.writer(response)
    writer.writerow(['title', 'slug', 'description', 'poster_url', 'duration', 'location', 'bookable', 'price'])

    for show in Show.objects.all():
        writer.writerow([
            show.title,
            show.slug or '',
            show.description,
            show.poster_url,
            show.duration or '',
            show.location.slug if show.location else '',
            show.bookable,
            show.price,
        ])

    return response


@login_required
@user_passes_test(is_admin)
def import_shows_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file:
            messages.error(request, "Aucun fichier sélectionné !")
            return redirect('reservations:dashboard')

        reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))
        created, updated = 0, 0

        for row in reader:
            location = Location.objects.filter(slug=row.get('location')).first() if row.get('location') else None

            show, was_created = Show.objects.update_or_create(
                title=row['title'],
                defaults={
                    'slug': row.get('slug') or None,
                    'description': row.get('description', ''),
                    'poster_url': row.get('poster_url', ''),
                    'duration': row.get('duration') or None,
                    'location': location,
                    'bookable': row.get('bookable', '').strip().lower() in ('true', '1', 'oui'),
                    'price': row.get('price') or 0,
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        messages.success(request, f"Import terminé : {created} spectacle(s) créé(s), {updated} mis à jour.")

    return redirect('reservations:dashboard')


@login_required
@user_passes_test(is_admin)
def sync_shows_webservice(request):
    if request.method == 'POST':
        try:
            created, updated = sync_shows_from_webservice()
            messages.success(request, f"Synchronisation terminée : {created} créé(s), {updated} mis à jour.")
        except WebserviceSyncError as error:
            messages.error(request, str(error))

    return redirect('reservations:dashboard')


# --- PressArticle (critique de presse) ---

def press_article_index(request):
    articles = PressArticle.objects.filter(published=True)

    return render(request, 'press_article/index.html', {
        'articles': articles,
        'title': 'Critiques de presse',
    })


def show_press_article(request, id):
    article = get_object_or_404(PressArticle, id=id)

    return render(request, 'press_article/show.html', {
        'article': article,
    })


@login_required
@permission_required('reservations.add_pressarticle', raise_exception=True)
def press_article_create(request):
    form = PressArticleForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)
            article.critic = request.user
            article.published = False
            article.save()
            messages.success(request, "Article envoyé avec succès, en attente de publication par le producteur.")

            return redirect('reservations:press_article_index')
        else:
            messages.error(request, "Échec de l'envoi de l'article !")

    return render(request, 'press_article/create.html', {
        'form': form,
    })


@login_required
def press_article_edit(request, id):
    article = get_object_or_404(PressArticle, id=id, critic=request.user)
    form = PressArticleForm(request.POST or None, instance=article)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                article = form.save(commit=False)
                article.published = False
                article.save()
                messages.success(request, "Article modifié avec succès, en attente de nouvelle publication.")

                return redirect('reservations:show_press_article', id=article.id)
            else:
                messages.error(request, "Échec de la modification de l'article !")

    return render(request, 'press_article/edit.html', {
        'form': form,
        'article': article,
    })


@login_required
def press_article_delete(request, id):
    article = get_object_or_404(PressArticle, id=id, critic=request.user)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            article.delete()
            messages.success(request, "Article supprimé avec succès.")

            return redirect('reservations:press_article_index')
        else:
            messages.error(request, "Échec de la suppression de l'article !")

    return render(request, 'press_article/show.html', {
        'article': article,
    })


@login_required
def press_article_publish(request, id):
    article = get_object_or_404(PressArticle, id=id)
    is_producer_of_show = article.show.producer_id == request.user.id

    if not (is_producer_of_show or is_admin(request.user)):
        messages.error(request, "Vous n'avez pas l'autorisation de publier cet article !")
        return redirect('reservations:show_press_article', id=article.id)

    if request.method == 'POST':
        article.published = True
        article.save()
        messages.success(request, "Article publié avec succès.")

    return redirect('reservations:show_press_article', id=article.id)


# --- Espace producteur ---

@login_required
def producer_dashboard(request):
    shows = Show.objects.filter(producer=request.user)

    shows_stats = []
    for show in shows:
        stats = Reservation.objects.filter(representation__show=show).aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('price')),
        )
        shows_stats.append({
            'show': show,
            'total_quantity': stats['total_quantity'] or 0,
            'total_revenue': stats['total_revenue'] or 0,
        })

    return render(request, 'producer_dashboard.html', {
        'shows_stats': shows_stats,
        'pending_reviews': Review.objects.filter(show__producer=request.user, validated=False),
        'pending_articles': PressArticle.objects.filter(show__producer=request.user, published=False),
    })


# --- Demandes de role (CRITIC / PRODUCER) ---

@login_required
def role_request_create(request, role):
    if role not in RoleRequest.Role.values:
        messages.error(request, "Rôle inconnu.")
        return redirect('accounts:user-profile')

    if request.user.groups.filter(name=role).exists():
        messages.error(request, "Vous avez déjà ce rôle.")
        return redirect('accounts:user-profile')

    if RoleRequest.objects.filter(user=request.user, role=role, status=RoleRequest.Status.PENDING).exists():
        messages.error(request, "Vous avez déjà une demande en attente pour ce rôle.")
        return redirect('accounts:user-profile')

    if request.method == 'POST':
        RoleRequest.objects.create(
            user=request.user,
            role=role,
            message=request.POST.get('message', ''),
        )
        messages.success(request, "Demande envoyée, en attente de validation par l'administrateur.")

        return redirect('accounts:user-profile')

    return render(request, 'role_request/create.html', {
        'role': role,
        'role_label': dict(RoleRequest.Role.choices).get(role),
    })


@login_required
@user_passes_test(is_admin)
def role_request_approve(request, id):
    role_request = get_object_or_404(RoleRequest, id=id, status=RoleRequest.Status.PENDING)

    if request.method == 'POST':
        group = Group.objects.get(name=role_request.role)
        group.user_set.add(role_request.user)

        role_request.status = RoleRequest.Status.APPROVED
        role_request.reviewed_by = request.user
        role_request.reviewed_at = timezone.now()
        role_request.save()

        messages.success(request, f"Demande de {role_request.user.username} approuvée.")

    return redirect('reservations:dashboard')


@login_required
@user_passes_test(is_admin)
def role_request_reject(request, id):
    role_request = get_object_or_404(RoleRequest, id=id, status=RoleRequest.Status.PENDING)

    if request.method == 'POST':
        role_request.status = RoleRequest.Status.REJECTED
        role_request.reviewed_by = request.user
        role_request.reviewed_at = timezone.now()
        role_request.save()

        messages.success(request, f"Demande de {role_request.user.username} refusée.")

    return redirect('reservations:dashboard')
