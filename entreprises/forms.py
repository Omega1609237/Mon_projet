from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from .models import Entreprise

class InscriptionEntrepriseForm(UserCreationForm):
    nom_entreprise = forms.CharField(max_length=255)
    secteur_activite = forms.CharField(max_length=255)
    site_web = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'nom_entreprise', 'secteur_activite', 'site_web', 'description']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'entreprise'
        if commit:
            user.save()
            Entreprise.objects.create(
                user=user,
                nom_entreprise=self.cleaned_data['nom_entreprise'],
                secteur_activite=self.cleaned_data['secteur_activite'],
                site_web=self.cleaned_data['site_web'],
                description=self.cleaned_data['description']
            )
        return user

from django import forms
from .models import Offre

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'description', 'lieu', 'duree', 'date_limite']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-full'}),
            'lieu': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'duree': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'date_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-input mt-1 block w-full'}),
        }
# entreprises/forms.py

from django import forms
from etudiants.models import Candidature
from etudiants.models import Etudiant
from entreprises.models import Offre

class CandidatureEntrepriseForm(forms.ModelForm):
    etudiant = forms.ModelChoiceField(queryset=Etudiant.objects.all())
    offre = forms.ModelChoiceField(queryset=Offre.objects.all())

    class Meta:
        model = Candidature
        fields = ['etudiant', 'offre', 'cv', 'lettre_motivation']
        widgets = {
            'cv': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-300 p-2 rounded w-full'
            }),
            'lettre_motivation': forms.Textarea(attrs={
                'class': 'border border-gray-300 p-2 rounded w-full',
                'rows': 4,
            }),
        }

from django import forms

class ReponseEmailForm(forms.Form):
    sujet = forms.CharField(max_length=200, label="Sujet")
    message = forms.CharField(widget=forms.Textarea, label="Message")

# entreprises/forms.py
from django import forms
from .models import Entreprise

class EntrepriseProfilForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom_entreprise', 'secteur_activite', 'site_web', 'description']
        widgets = {
            'nom_entreprise': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'secteur_activite': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'site_web': forms.URLInput(attrs={'class': 'border p-2 w-full rounded'}),
            'description': forms.Textarea(attrs={'class': 'border p-2 w-full rounded'}),
        }
