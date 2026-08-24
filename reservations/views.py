from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Artist

# Create your views here.
def index(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>Accueil</h1><p>Bienvenue sur notre site.</p>.")

def contact(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>Contact</h1><p>Nous contacter.</p>.")

def about(request):
    return HttpResponse("<a href='/'>Accueil</a> | <a href='/contact/'>Contact</a>| <a href='/about/'>À propos</a> <br><h1>À propos</h1><p>Informations sur notre entreprise.</p>.")

def show_artist(request, id):
    artist = get_object_or_404(Artist, id=id)
    return HttpResponse(f"Ceci est la page de l'artiste : {artist.lastname} {artist.firstname}")
