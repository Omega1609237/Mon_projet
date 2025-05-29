# etudiants/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser  # Vérifie que tu importes bien CustomUser depuis ton app
from etudiants.models import Etudiant

class InscriptionForm(UserCreationForm):
    # user_type = forms.ChoiceField(
    #     choices=[
    #         ('etudiant', 'Étudiant'),
    #         ('entreprise', 'Entreprise'),
    #     ],
    #     label="Type d'utilisateur"
    # )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['prenom', 'nom', 'telephone', 'competence', 'cv','photo']

# etudiants/forms.py

from django import forms
from .models import Candidature

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv', 'lettre_motivation']
        widgets = {
            'cv': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-300 p-2 rounded w-full'
            }),
            'lettre_motivation': forms.Textarea(attrs={
                'placeholder': 'Écrivez votre lettre de motivation ici...',
                'class': 'border border-gray-300 p-2 rounded w-full',
                'rows': 5,
            }),
        }


# etudiants/forms.py
from django import forms
from .models import Etudiant

# etudiants/forms.py

class EtudiantProfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'cv', 'competence', 'telephone', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'prenom': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            # 'adresse': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'competence': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EtudiantProfilForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        etudiant = super().save(commit=False)
        if commit:
            etudiant.save()
            self.instance.user.email = self.cleaned_data['email']
            self.instance.user.save()
        return etudiant

