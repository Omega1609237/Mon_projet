from django.db import models

# Create your models here.
        

from django.db import models
from accounts.models import CustomUser

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='etudiant')
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    competence = models.TextField(blank=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    photo = models.ImageField(upload_to='photos_etudiants/', null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


from django.db import models
from django.conf import settings
from entreprises.models import Offre

class Candidature(models.Model):
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')
    date_candidature = models.DateTimeField(auto_now_add=True)
    lettre_motivation = models.TextField()
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    
    
    def competences_list(self):
        return [comp.strip() for comp in self.competence.split(",") if comp.strip()]
        
    def __str__(self):
        return f"{self.etudiant.username} - {self.offre.titre}"
        

from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=Candidature)
def supprimer_cv(sender, instance, **kwargs):
    if instance.cv:
        instance.cv.delete(False)
