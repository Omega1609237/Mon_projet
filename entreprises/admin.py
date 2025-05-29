from django.contrib import admin
from .models import Candidature

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'offre', 'date_candidature')
