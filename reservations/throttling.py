from rest_framework.throttling import SimpleRateThrottle

from .models import UserMeta


def get_affiliate_tier(user):
    try:
        return user.usermeta.affiliate_tier
    except UserMeta.DoesNotExist:
        return UserMeta.AffiliateTier.NONE


class AffiliateTierThrottle(SimpleRateThrottle):
    """
    Limite le nombre de requêtes API par jour selon le palier d'affiliation
    (UserMeta.affiliate_tier) de l'utilisateur authentifié : Free, Starter,
    Premium. Un utilisateur non affilié (tier "none", valeur par défaut)
    ou anonyme n'est pas concerné par cette limite (la lecture publique
    anonyme est gérée par ailleurs via DjangoModelPermissionsOrAnonReadOnly).
    """
    scope = 'affiliate'

    TIER_RATES = {
        UserMeta.AffiliateTier.FREE: '20/day',
        UserMeta.AffiliateTier.STARTER: '200/day',
        UserMeta.AffiliateTier.PREMIUM: '2000/day',
    }

    def get_rate(self):
        return self.TIER_RATES[UserMeta.AffiliateTier.FREE]

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            ident = self.get_ident(request)
        else:
            ident = request.user.pk

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }

    def allow_request(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return True

        tier = get_affiliate_tier(user)

        if tier == UserMeta.AffiliateTier.NONE:
            return True

        self.num_requests, self.duration = self.parse_rate(self.TIER_RATES.get(tier, self.get_rate()))

        return super().allow_request(request, view)
