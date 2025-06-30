from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription_entreprise, name='inscription_entreprise'),
    path('connexion/', views.connexion_entreprise, name='connexion_entreprise'),
    path('dashboard/', views.tableau_de_bord_entreprise, name='tableau_de_bord_entreprise'),
    path('publier-offre/', views.publier_offre, name='publier_offre'),
    path('voir-candidatures/', views.voir_candidatures, name='voir_candidatures'),
    path('voir-profil-etudiant/<int:etudiant_id>/', views.voir_profil_etudiant, name='voir_profil_etudiant'),
    path('repondre/<int:candidature_id>/', views.repondre_etudiant, name='repondre_etudiant'),
    path('mes-offres/', views.mes_offres, name='mes_offres'),
    path('offre/<int:offre_id>/modifier/', views.modifier_offre, name='modifier_offre'),
    path('offre/<int:offre_id>/supprimer/', views.supprimer_offre, name='supprimer_offre'),
    path('modifier-profil/', views.modifier_profil_entreprise, name='modifier_profil_entreprise'),
    path('profil/', views.voir_profil_entreprise, name='profil_entreprise'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/<int:etudiant_id>/', views.profil_etudiant, name='profil_etudiant'),


]
