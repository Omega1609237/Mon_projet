from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home, dashboard_global, tableau_de_bord_etudiant
from etudiants.views import connexion_etudiant
#from etudiants.views import connexion

urlpatterns = [
    path('', home, name='home'),

    # Inscription et Connexion
    path('inscription/etudiant/', views.inscription_etudiant, name='inscription_etudiant'),
    path('connexion/etudiant/', views.connexion_etudiant, name='connexion_etudiant'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Accueil étudiant
    path('accueil/', views.accueil_etudiant, name='accueil_etudiant'),

    # Tableau de bord
    path('dashboard/', dashboard_global, name='dashboard_global'),
    path('etudiants/dashboard/', tableau_de_bord_etudiant, name='tableau_de_bord_etudiant'),

    # Offres de stages
    path('offres/', views.voir_offres, name='voir_offres'),
    path('offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),
    path('postulation/succes/', views.postulation_succes, name='postulation_succes'),
    path('offres/<int:offre_id>/', views.detail_offre, name='detail_offre'),
    path('offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),

    # Profil étudiant
    path('profil/', views.profil_etudiant, name='profil_etudiant'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),

    # Mes candidatures
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('retirer-candidature/<int:candidature_id>/', views.retirer_candidature, name='retirer_candidature'),
    path('candidature/modifier/<int:candidature_id>/', views.modifier_candidature, name='modifier_candidature'),
    path('candidature/supprimer/<int:candidature_id>/', views.confirmer_suppression_candidature, name='confirmer_suppression_candidature'),


    #path('connexion/', views.connexion_etudiant, name='connexion'),
    path('connexion/', views.connexion_etudiant, name='connexion_etudiant'),
    #path('dashboard/', dashboard_global, name='dashboard_global'),

    


]
