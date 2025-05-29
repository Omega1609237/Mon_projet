from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm, EtudiantForm
from .models import Etudiant
from entreprises.models import Offre
from django.contrib import messages



# Page d'accueil
def home(request):
    return render(request, 'home.html')

# Inscription étudiant
# from django.shortcuts import render, redirect
# from .forms import InscriptionForm, EtudiantForm
# from etudiants.models import Etudiant
# from accounts.models import CustomUser

# def inscription_etudiant(request):
#     if request.method == 'POST':
#         user_form = InscriptionForm(request.POST)
#         etudiant_form = EtudiantForm(request.POST, request.FILES)

#         if user_form.is_valid() and etudiant_form.is_valid():
#             user = user_form.save(commit=False)
#             user.user_type = 'etudiant'  # Assure-toi qu'on crée bien un étudiant
#             user.save()

#             # Empêche la création d'un profil étudiant s'il existe déjà
#             if not Etudiant.objects.filter(user=user).exists():
#                 etudiant = etudiant_form.save(commit=False)
#                 etudiant.user = user
#                 etudiant.save()

#             return redirect('connexion_etudiant')
#     else:
#         user_form = InscriptionForm()
#         etudiant_form = EtudiantForm()

#     return render(request, 'etudiants/inscription_etudiant.html', {
#         'form': user_form,
#         'etudiant_form': etudiant_form
#     })

# from django.shortcuts import render, redirect
# from accounts.forms import InscriptionForm
# from etudiants.forms import EtudiantForm
# from accounts.models import CustomUser
# from etudiants.models import Etudiant

from django.db import IntegrityError

def inscription_etudiant(request):
    if request.method == 'POST':
        user_form = InscriptionForm(request.POST)
        etudiant_form = EtudiantForm(request.POST, request.FILES)

        if user_form.is_valid() and etudiant_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.user_type = 'etudiant'
                user.save()

                etudiant = etudiant_form.save(commit=False)
                etudiant.user = user
                etudiant.save()

                return redirect('connexion_etudiant')

            except IntegrityError:
                etudiant_form.add_error(None, "Erreur : un compte ou profil similaire existe déjà.")
    else:
        user_form = InscriptionForm()
        etudiant_form = EtudiantForm()

    return render(request, 'etudiants/inscription_etudiant.html', {
        'form': user_form,
        'etudiant_form': etudiant_form
    })




# Connexion étudiant
def connexion_etudiant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.user_type == 'etudiant':
            login(request, user)
            return redirect('accueil_etudiant')
        else:
            # Optionnel : afficher une erreur
            return render(request, 'etudiants/connexion_etudiant.html', {
                'erreur': "Identifiants invalides ou compte non étudiant."
            })
    return render(request, 'etudiants/connexion_etudiant.html')



# Tableau de bord étudiant
@login_required
def tableau_de_bord_etudiant(request):
    return render(request, 'etudiants/accueil_etudiant.html')

# Dashboard global
def dashboard_global(request):
    return render(request, 'tableau_de_bord.html')


from django.shortcuts import render
from entreprises.models import Offre

def voir_offres(request):
    offres = Offre.objects.all().order_by('-date_creation')  # Tu peux trier comme tu veux
    return render(request, 'etudiants/voir_offres.html', {'offres': offres})


def postulation_succes(request):
    return render(request, 'etudiants/postulation_succes.html')


# etudiants/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Etudiant
from .forms import EtudiantProfilForm

@login_required
def profil_etudiant(request):
    etudiant = request.user.etudiant
    form = EtudiantProfilForm(instance=etudiant)

    return render(request, 'etudiants/profil_etudiant.html', {
        'form': form,
        'etudiant': etudiant
    })

@login_required
def modifier_profil(request):
    etudiant = request.user.etudiant

    if request.method == 'POST':
        form = EtudiantProfilForm(request.POST, request.FILES, instance=etudiant, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil_etudiant')
    else:
        form = EtudiantProfilForm(instance=etudiant, user=request.user)

    return render(request, 'etudiants/modifier_profil.html', {'form': form})




# Mes candidatures
@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(etudiant=request.user.etudiant)
    return render(request, 'etudiants/mes_candidatures.html', {'candidatures': candidatures})

# Accueil étudiant
def accueil_etudiant(request):
    return render(request, 'etudiants/accueil_etudiant.html')

from django.shortcuts import get_object_or_404
from entreprises.models import Offre

def detail_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    entreprise = offre.entreprise  # On accède à l’entreprise qui a publié l’offre
    return render(request, 'etudiants/detail_offre.html', {
        'offre': offre,
        'entreprise': entreprise
    })

from .forms import CandidatureForm
from .models import Candidature

@login_required
def postuler_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    # Vérifie si déjà candidat
    deja_postule = Candidature.objects.filter(etudiant=request.user, offre=offre).exists()
    if deja_postule:
        messages.info(request, "Vous avez déjà postulé à cette offre.")
        return redirect('detail_offre', offre_id=offre_id)

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.etudiant = request.user
            candidature.offre = offre
            candidature.save()
            messages.success(request, "Votre candidature a été envoyée avec succès.")
            return render(request, 'etudiants/postulation_success.html', {'offre': offre})

    else:
        form = CandidatureForm()

    return render(request, 'etudiants/postuler_offre.html', {
        'form': form,
        'offre': offre
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from etudiants.models import Candidature  

@login_required
def mes_candidatures(request):
    candidatures = Candidature.objects.filter(etudiant=request.user).select_related('offre')
    return render(request, 'etudiants/mes_candidatures.html', {'candidatures': candidatures})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from etudiants.models import Candidature

@login_required
def retirer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)
    candidature.delete()
    messages.success(request, "Votre candidature a été retirée avec succès.")
    return redirect('mes_candidatures')

from django.shortcuts import get_object_or_404, redirect, render
from .models import Candidature
from .forms import CandidatureForm  # Tu dois créer ce formulaire si ce n’est pas déjà fait
from django.contrib.auth.decorators import login_required

@login_required
def modifier_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)

    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES, instance=candidature)
        if form.is_valid():
            form.save()
            return redirect('mes_candidatures')
    else:
        form = CandidatureForm(instance=candidature)

    return render(request, 'etudiants/modifier_candidature.html', {'form': form})


@login_required
def confirmer_suppression_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id, etudiant=request.user)

    if request.method == 'POST':
        candidature.delete()
        return redirect('mes_candidatures')

    return render(request, 'etudiants/confirmer_suppression.html', {'candidature': candidature})
