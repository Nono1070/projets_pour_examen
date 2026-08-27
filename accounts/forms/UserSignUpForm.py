from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from reservations.models import UserMeta


class UserSignUpForm(UserCreationForm):

    class Language(models.TextChoices):
        NONE = "", "Choisissez votre langue"
        FRENCH = "fr", "Français"
        ENGLISH = "en", "English"
        DUTCH = "nl", "Nederlands"

    # Définir les types de champs
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField()

    # Ajout des champs de données personnelles supplémentaires
    langue = forms.ChoiceField(choices=Language)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmation du mot de passe'
        self.fields['first_name'].label = 'Prénom'
        self.fields['last_name'].label = 'Nom'

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre compte.")

        return email

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'langue',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Ajout de l'utilisateur au groupe MEMBER => rôle de membre
        member_group = Group.objects.get(name='MEMBER')
        member_group.user_set.add(user)

        if self.cleaned_data['langue']:
            user_meta = UserMeta(**{
                'langue': self.cleaned_data['langue'],
            })

            # Mise à jour de la relation one-to-one
            user_meta.user = user
            user_meta.save()

        return user
