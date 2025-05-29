# etudiants/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Etudiant

@receiver(post_save, sender=CustomUser)
def create_etudiant_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "etudiant":
        Etudiant.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_etudiant_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'etudiant':
        Etudiant.objects.create(user=instance)
