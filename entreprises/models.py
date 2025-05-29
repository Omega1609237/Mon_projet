from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Entreprise(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length=255)
    secteur_activite = models.CharField(max_length=255)
    site_web = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom_entreprise
class Offre(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='offres')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    duree = models.CharField(max_length=50)
    date_limite = models.DateField()
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

from django.db import models
from etudiants.models import Etudiant  # adapte selon ton app
from entreprises.models import Offre   # vérifie bien que le modèle Offre existe
from django.utils import timezone

class Candidature(models.Model):
    
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    lettre_motivation = models.TextField()
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    date_candidature = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.etudiant.user.username} → {self.offre.titre}"
