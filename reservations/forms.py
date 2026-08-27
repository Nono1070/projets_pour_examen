from django import forms

from .models import Artist, Type, Locality, Location, Show, Representation, Review, Reservation, PressArticle


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'firstname',
            'lastname',
        ]


class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = [
            'type',
        ]


class LocalityForm(forms.ModelForm):

    class Meta:
        model = Locality
        fields = [
            'locality',
            'postal_code',
        ]


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = [
            'slug',
            'designation',
            'address',
            'website',
            'phone',
        ]


class ShowForm(forms.ModelForm):

    class Meta:
        model = Show
        fields = [
            'slug',
            'title',
            'description',
            'poster_url',
            'duration',
            'location',
            'bookable',
            'price',
            'producer',
        ]


class RepresentationForm(forms.ModelForm):

    class Meta:
        model = Representation
        fields = [
            'show',
            'schedule',
            'location',
        ]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'show',
            'review',
            'stars',
        ]


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = [
            'representation',
            'quantity',
        ]


class PressArticleForm(forms.ModelForm):

    class Meta:
        model = PressArticle
        fields = [
            'show',
            'title',
            'content',
            'url',
        ]
