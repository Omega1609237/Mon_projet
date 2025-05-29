from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Etudiant

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'user', 'telephone', 'competence')
    search_fields = ('prenom', 'nom', 'user__username')

admin.site.register(Etudiant, EtudiantAdmin)
