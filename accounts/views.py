from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum, F

from reservations.models import Reservation, Review, PressArticle, UserMeta

from .forms import UserSignUpForm, UserUpdateForm


class UserSignUpView(UserPassesTestMixin, CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous êtes déjà inscrit !")
        return redirect('reservations:index')


class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("accounts:user-profile")
    template_name = "user/update.html"

    def test_func(self):
        pk_in_url = self.kwargs['pk']
        return self.request.user.is_authenticated and self.request.user.id == pk_in_url or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas l'autorisation d'accéder à cette page !")
        return redirect('accounts:user-profile')


@login_required
def profile(request):
    languages = {
        "fr": "Français",
        "en": "English",
        "nl": "Nederlands",
    }

    try:
        user_language = languages.get(request.user.usermeta.langue)
    except UserMeta.DoesNotExist:
        user_language = None

    reservations_stats = Reservation.objects.filter(user=request.user).aggregate(
        total_quantity=Sum('quantity'),
        total_spent=Sum(F('quantity') * F('price')),
    )

    return render(request, 'user/profile.html', {
        "user_language": user_language,
        "reservations_count": Reservation.objects.filter(user=request.user).count(),
        "reservations_total_quantity": reservations_stats['total_quantity'] or 0,
        "reservations_total_spent": reservations_stats['total_spent'] or 0,
        "reviews_count": Review.objects.filter(user=request.user).count(),
        "press_articles_count": PressArticle.objects.filter(critic=request.user).count(),
    })


@login_required
def delete(request, pk):
    if request.method == 'POST':
        if request.user.id == pk or request.user.is_superuser:
            user = User.objects.get(id=pk)
            was_self = user.id == request.user.id
            user.delete()

            if was_self:
                logout(request)

            return redirect('reservations:index')

        messages.error(request, "Vous n'avez pas l'autorisation de supprimer ce compte !")

    return redirect('accounts:user-profile')
