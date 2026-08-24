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
]
