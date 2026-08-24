from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Artist, Type, Locality, Location, Show, UserMeta,
    Representation, Review, ArtistType, ArtistTypeShow,
)


# Personnalisation de l'affichage pour Artist
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')  # Colonnes à afficher
    search_fields = ('firstname', 'lastname')  # Barre de recherche


# Personnalisation pour Show
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'bookable', 'price')  # Colonnes à afficher
    search_fields = ('title',)  # Barre de recherche


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Show, ShowAdmin)
admin.site.register(Representation)
admin.site.register(Review)
admin.site.register(ArtistType)
admin.site.register(ArtistTypeShow)

admin.site.index_title = "Projet Réservations"
admin.site.index_header = "Projet Réservations"
admin.site.site_title = "Spectacles"


# Ajout des informations de profil (UserMeta) dans la fiche User de Django Admin
class UserMetaInline(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = "user_meta"


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
