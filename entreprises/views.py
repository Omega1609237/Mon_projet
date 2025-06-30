from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import InscriptionEntrepriseForm
from accounts.forms import ConnexionForm  # si tu l'as déjà créé

def inscription_entreprise(request):
    if request.method == 'POST':
        form = InscriptionEntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion_entreprise')
    else:
        form = InscriptionEntrepriseForm()
    return render(request, 'entreprises/inscription_entreprise.html', {'form': form})


def connexion_entreprise(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.user_type == 'entreprise':
                login(request, user)
                return redirect('tableau_de_bord_entreprise') 
    else:
        form = ConnexionForm()
    return render(request, 'entreprises/connexion_entreprise.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Entreprise

@login_required
def tableau_de_bord_entreprise(request):
    entreprise = Entreprise.objects.get(user=request.user)
    return render(request, 'entreprises/tableau_de_bord_entreprise.html', {'entreprise': entreprise})

from django.shortcuts import redirect
from .forms import OffreForm
from django.contrib import messages

@login_required
def publier_offre(request):
    entreprise = Entreprise.objects.get(user=request.user)

    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = entreprise
            offre.save()
            messages.success(request, "Offre publiée avec succès ✅")
            return redirect('tableau_de_bord_entreprise')
    else:
        form = OffreForm()

    return render(request, 'entreprises/publier_offre.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from etudiants.models import Candidature  # adapte si l’app s'appelle différemment
from .models import Entreprise
from .models import Offre

@login_required
def voir_candidatures(request):
    entreprise = request.user.entreprise
    offres = Offre.objects.filter(entreprise=entreprise)
    candidatures = Candidature.objects.filter(offre__in=offres).select_related('etudiant', 'offre')

    return render(request, 'entreprises/voir_candidatures.html', {
        'candidatures': candidatures
    })

from django.shortcuts import get_object_or_404
from etudiants.models import Etudiant  # si ton modèle Etudiant est dans l'app etudiants

@login_required
def voir_profil_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    return render(request, 'entreprises/voir_profil_etudiant.html', {
        'etudiant': etudiant
    })

from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from etudiants.models import Candidature
from .forms import ReponseEmailForm  # Form avec 'sujet' et 'message'

@login_required
def repondre_etudiant(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    etudiant = candidature.etudiant
    entreprise_email = request.user.email  # Email de l'entreprise connectée

    if request.method == 'POST':
        form = ReponseEmailForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            destinataire = etudiant.email

            email = EmailMessage(
                subject=sujet,
                body=message,
                from_email="MonStage <ecclesiasteomega1@gmail.com>",  # Ton adresse SMTP
                to=[destinataire],
                reply_to=[entreprise_email],  # Réponse vers l’entreprise
            )
            email.send()
            messages.success(request, "L’email a bien été envoyé à l’étudiant.")
            return redirect('voir_candidatures')
    else:
        form = ReponseEmailForm()

    return render(request, 'entreprises/repondre_etudiant.html', {
        'form': form,
        'etudiant_email': etudiant.email
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Offre

@login_required
def mes_offres(request):
    entreprise = request.user.entreprise  # Assure-toi que l'utilisateur a un profil entreprise
    offres = Offre.objects.filter(entreprise=entreprise).order_by('-date_creation')
    return render(request, 'entreprises/mes_offres.html', {'offres': offres})

from django.shortcuts import get_object_or_404, redirect
from .forms import OffreForm

@login_required
def modifier_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id, entreprise=request.user.entreprise)
    if request.method == 'POST':
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('mes_offres')
    else:
        form = OffreForm(instance=offre)
    return render(request, 'entreprises/modifier_offre.html', {'form': form, 'offre': offre})

@login_required
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id, entreprise=request.user.entreprise)
    if request.method == 'POST':
        offre.delete()
        return redirect('mes_offres')
    return render(request, 'entreprises/confirmer_suppression.html', {'offre': offre})
# entreprises/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EntrepriseProfilForm
from .models import Entreprise

@login_required
def modifier_profil_entreprise(request):
    entreprise = get_object_or_404(Entreprise, user=request.user)

    if request.method == 'POST':
        form = EntrepriseProfilForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('tableau_de_bord_entreprise')
    else:
        form = EntrepriseProfilForm(instance=entreprise)

    return render(request, 'entreprises/modifier_profil_entreprise.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Entreprise

@login_required
def voir_profil_entreprise(request):
    entreprise = get_object_or_404(Entreprise, user=request.user)
    return render(request, 'entreprises/voir_profil_entreprise.html', {'entreprise': entreprise})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from etudiants.models import Etudiant

@login_required
def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'entreprises/liste_etudiants.html', {'etudiants': etudiants})

# entreprises/views.py
from django.shortcuts import get_object_or_404

@login_required
def profil_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    return render(request, 'entreprises/profil_etudiant.html', {'etudiant': etudiant})
