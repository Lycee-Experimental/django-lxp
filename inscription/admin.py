from django.contrib import admin
from .models import BaseEleve, Departement, Commune
# Register your models here.
admin.site.register(BaseEleve)
admin.site.register(Departement)
admin.site.register(Commune)
