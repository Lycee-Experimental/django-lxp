import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import BaseEleve


class ListeEleveTableau(tables.Table):
    """Affiche le tableau de recherche des inscrit.e.s."""
    class Meta:
        # L'allure du tableau
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table table-striped table-hover"}
        # Les données à utiliser
        model = BaseEleve
        # Les champs à afficher
        fields = (
            "last_name",
            "first_name",
        )
        # Le texte si aucune entrées
        empty_text = _(
            "Aucun.e élève ne correspond aux critères de recherche."
        )
        # Le nombre d'entrée max par page
        per_page = 20