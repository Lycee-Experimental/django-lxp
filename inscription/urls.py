from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from djangoLxp import settings
from .views import InscriptionView, FormulaireInscription, fiche, fiche_pdf, carto, ajout_allergie, ajout_dys

app_name = 'inscription'

urlpatterns = [
    path('inscriptions', login_required(InscriptionView.as_view()), name="inscriptions"),
    path('', FormulaireInscription.as_view(), name='formulaire'),
    path('<int:id>/<hash>', FormulaireInscription.as_view(), name='update'),
    path('fiche/<int:id>/<hash>', fiche, name='fiche'),
    path('pdf/<int:id>/<hash>', fiche_pdf, name='pdf'),
    path('carto', carto, name='carto'),
    path('allergie', ajout_allergie, name='allergie'),
    path('dys', ajout_dys, name='dys'),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()