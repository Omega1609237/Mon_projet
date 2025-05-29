from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST  # ⛔ Empêche les requêtes GET (protection)
def deconnexion(request):
    logout(request)
    return redirect('login')  # redirige vers la page de connexion ou accueil
