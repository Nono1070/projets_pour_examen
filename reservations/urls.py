from django.urls import path
from . import views
from .api_views import ArtistListCreateView, ArtistRetrieveUpdateDestroyView, ShowListView, ShowRetrieveView
from .feeds import UpcomingRepresentationsFeed

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cookies/accepter/', views.accept_cookies, name='accept_cookies'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/export/', views.export_shows_csv, name='export_shows_csv'),
    path('dashboard/import/', views.import_shows_csv, name='import_shows_csv'),
    path('rss/representations/', UpcomingRepresentationsFeed(), name='representations_feed'),

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

    path('representations/', views.representation_index, name='representation_index'),
    path('representation/create/', views.representation_create, name='representation_create'),
    path('representation/edit/<int:id>/', views.representation_edit, name='representation_edit'),
    path('representation/delete/<int:id>/', views.representation_delete, name='representation_delete'),
    path('representation/<int:id>/', views.show_representation, name='show_representation'),

    path('critiques/', views.review_index, name='review_index'),
    path('critique/create/', views.review_create, name='review_create'),
    path('critique/edit/<int:id>/', views.review_edit, name='review_edit'),
    path('critique/delete/<int:id>/', views.review_delete, name='review_delete'),
    path('critique/valider/<int:id>/', views.review_validate, name='review_validate'),
    path('critique/<int:id>/', views.show_review, name='show_review'),

    path('reservations/', views.reservation_index, name='reservation_index'),
    path('reservation/create/', views.reservation_create, name='reservation_create'),
    path('reservation/edit/<int:id>/', views.reservation_edit, name='reservation_edit'),
    path('reservation/delete/<int:id>/', views.reservation_delete, name='reservation_delete'),
    path('reservation/<int:id>/', views.show_reservation, name='show_reservation'),

    path('critiques-presse/', views.press_article_index, name='press_article_index'),
    path('critique-presse/create/', views.press_article_create, name='press_article_create'),
    path('critique-presse/edit/<int:id>/', views.press_article_edit, name='press_article_edit'),
    path('critique-presse/delete/<int:id>/', views.press_article_delete, name='press_article_delete'),
    path('critique-presse/publier/<int:id>/', views.press_article_publish, name='press_article_publish'),
    path('critique-presse/<int:id>/', views.show_press_article, name='show_press_article'),

    path('producteur/', views.producer_dashboard, name='producer_dashboard'),

    path('api/artists/', ArtistListCreateView.as_view(), name='artist-api-list'),
    path('api/artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist-api-detail'),
    path('api/shows/', ShowListView.as_view(), name='show-api-list'),
    path('api/shows/<int:pk>/', ShowRetrieveView.as_view(), name='show-api-detail'),
]
