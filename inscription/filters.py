from .models import BaseEleve
import django_filters

class ListeEleveFiltre(django_filters.FilterSet):
    """
    Classe facilitant le filtrage de la liste d'élève, utilisée dans une PagedFilteredTableView
    """
    nom = django_filters.CharFilter(lookup_expr='icontains')
    # Définit la lookup expression, pour que la recherche fonctionne même si le terme n'est pas exact
    prenom = django_filters.CharFilter(lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        """Bidouille pour redéfinir le label des champs du formulaire de recherche."""
        super(ListeEleveFiltre, self).__init__(*args, **kwargs)
        self.filters['nom'].label = "Nom"
        self.filters['prenom'].label = "Prénom" 
        self.filters['gb_annee_en_cours'].label = "GB" 

    class Meta:
        """Définition des champs de la base élève dans lesquels effectuer la recherche"""
        model = BaseEleve
        fields = ['gb_annee_en_cours','nom','prenom']
        order_by = ["nom"]







