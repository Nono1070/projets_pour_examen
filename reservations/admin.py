from django.contrib import admin

# Register your models here.
from .models import Artist, Type, Locality, Location, Show

# Personnalisation de l'affichage pour Artist
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')# Colonnes à afficher
    search_fields = ('firstname', 'lastname')# Barre de recherche

# Personnalisation pour Show
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'bookable', 'price')# Colonnes à afficher
    search_fields = ('title',) # Barre de recherche
    
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Show, ShowAdmin)

