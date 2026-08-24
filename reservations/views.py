from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Artist
from .forms import ArtistForm

# Create your views here.
def index(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>Accueil</h1><p>Bienvenue sur notre site.</p>.")

def contact(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>Contact</h1><p>Nous contacter.</p>.")

def about(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>À propos</h1><p>Informations sur notre entreprise.</p>.")


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
    artists = Artist.objects.filter(types__type__iexact=type_name)
    title = f"Artistes de type : {type_name}"

    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': title,
        'query': '',
    })
