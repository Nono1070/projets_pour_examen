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


class ShowProposalForm(forms.ModelForm):
    """Utilise par un producteur pour proposer un nouveau spectacle. Pas de champ
    producer (auto-assigne au producteur connecte) ni published (reste False
    jusqu'a validation par un admin)."""

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
    """Le membre ne peut critiquer que les spectacles pour lesquels il a
    reserve une place (PID : "commenter les spectacles auxquels il a
    assiste") - le champ show n'affiche que ces spectacles-la."""

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['show'].queryset = Show.objects.filter(
                representations__reservations__user=user
            ).distinct()

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
            'photo_url',
            'content',
            'url',
        ]
