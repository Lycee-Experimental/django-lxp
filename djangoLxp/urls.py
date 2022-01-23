from django.urls import path, include
from django.contrib import admin
from django.urls import re_path as url
from inscription.models import Commune
from inscription.views import AutocompleteCommune, AutocompletePays, AutocompleteDepartement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inscription.urls')),
    path('captcha/', include('captcha.urls')),
    url('^linked_data/$', AutocompleteCommune.as_view(model=Commune), name='linked_data'),
    url('^pays/$', AutocompletePays.as_view(), name='pays'),
    url('^departement/$', AutocompleteDepartement.as_view(), name='departement'),


]