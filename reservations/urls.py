from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('artistes/', views.artist_index, name='artist_index'),
    path('artiste/create/', views.artist_create, name='artist_create'),
    path('artist/<int:id>/', views.show_artist, name='show_artist'),
]
