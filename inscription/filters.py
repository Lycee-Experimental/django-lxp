import django_filters
from .models import BaseEleve


class ListeEleveFiltre(django_filters.FilterSet):
    class Meta:
        model = BaseEleve
        fields = {
            "last_name": ["icontains"],
            "first_name": ["exact"],
        }
        order_by = ["last_name"]
