from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Artist, Type, Locality, Location, Show, Representation, Review, Reservation
from .forms import ArtistForm, TypeForm, LocalityForm, LocationForm, ShowForm, RepresentationForm, ReviewForm, ReservationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
    shows = Show.objects.all()

    return render(request, 'show/index.html', {
        'shows': shows,
        'title': 'Liste des spectacles',
    })


def show_show(request, id):
    show = get_object_or_404(Show, id=id)

    return render(request, 'show/show.html', {
        'show': show,
    })


@login_required
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
