from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('artistes/', views.artist_index, name='artist_index'),
    path('artiste/create/', views.artist_create, name='artist_create'),
    path('artiste/edit/<int:id>/', views.artist_edit, name='artist_edit'),
    path('artiste/delete/<int:id>/', views.artist_delete, name='artist_delete'),
    path('artistes/type/<str:type_name>/', views.artist_by_type, name='artist_by_type'),

    path('artist/<int:id>/', views.show_artist, name='show_artist'),

    path('types/', views.type_index, name='type_index'),
    path('type/create/', views.type_create, name='type_create'),
    path('type/edit/<int:id>/', views.type_edit, name='type_edit'),
    path('type/delete/<int:id>/', views.type_delete, name='type_delete'),
    path('type/<int:id>/', views.show_type, name='show_type'),

    path('localites/', views.locality_index, name='locality_index'),
    path('localite/create/', views.locality_create, name='locality_create'),
    path('localite/edit/<int:id>/', views.locality_edit, name='locality_edit'),
    path('localite/delete/<int:id>/', views.locality_delete, name='locality_delete'),
    path('localite/<int:id>/', views.show_locality, name='show_locality'),

    path('lieux/', views.location_index, name='location_index'),
    path('lieu/create/', views.location_create, name='location_create'),
    path('lieu/edit/<int:id>/', views.location_edit, name='location_edit'),
    path('lieu/delete/<int:id>/', views.location_delete, name='location_delete'),
    path('lieu/<int:id>/', views.show_location, name='show_location'),

    path('spectacles/', views.show_index, name='show_index'),
    path('spectacle/create/', views.show_create, name='show_create'),
    path('spectacle/edit/<int:id>/', views.show_edit, name='show_edit'),
    path('spectacle/delete/<int:id>/', views.show_delete, name='show_delete'),
    path('spectacle/<int:id>/', views.show_show, name='show_show'),
]
