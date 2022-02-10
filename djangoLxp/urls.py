from django.urls import path, include
from django.contrib import admin
from django.urls import re_path as url
from inscription.models import Commune
from inscription.views import AutocompleteCommune, AutocompletePays, AutocompleteDepartement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inscription.urls')),
    path('captcha/', include('captcha.urls')),
    url('^commune/$', AutocompleteCommune.as_view(model=Commune), name='commune'),
    url('^pays/$', AutocompletePays.as_view(), name='pays'),
    url('^departement/$', AutocompleteDepartement.as_view(), name='departement'),
    url('^mee/$', AutocompleteMEE.as_view(), name='mee'),
]