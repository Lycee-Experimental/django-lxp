import django_filters
from .models import BaseEleve


class ListeEleveFiltre(django_filters.FilterSet):
    class Meta:
        model = BaseEleve
        fields = {
            "nom": ["icontains"],
            "prenom": ["exact"],
        }
        order_by = ["nom"]
