from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Artist, Show
from .serializers import ArtistSerializer, ShowSerializer
from .throttling import AffiliateTierThrottle


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    throttle_classes = [AffiliateTierThrottle]


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    throttle_classes = [AffiliateTierThrottle]


class ShowListView(generics.ListAPIView):
    """Catalogue en lecture seule, destine aux affilies (API affilies)."""
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    throttle_classes = [AffiliateTierThrottle]


class ShowRetrieveView(generics.RetrieveAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    throttle_classes = [AffiliateTierThrottle]
