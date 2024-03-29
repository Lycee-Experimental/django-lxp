from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from djangoLxp import settings
from .views import InscriptionRechercheView, InscriptionTableView, FormulaireInscription, export_csv, fiche, fiche_pdf, \
    carto, ajout_allergie, ajout_dys, validation, table

app_name = 'inscription'

urlpatterns = [
    path('inscriptions', login_required(InscriptionRechercheView.as_view()), name="inscriptions"),
    path('inscriptions_table', login_required(InscriptionTableView.as_view()), name="inscriptions_table"),
    path('', FormulaireInscription.as_view(), name='formulaire'),
    path('<int:id>/<hash>', FormulaireInscription.as_view(), name='update'),
    path('fiche/<int:id>/<hash>', fiche, name='fiche'),
    path('pdf/<int:id>/<hash>', fiche_pdf, name='pdf'),
    path('validation/<int:id>/<hash>', validation, name='validation'),
    path('carto', carto, name='carto'),
    path('allergie', ajout_allergie, name='allergie'),
    path('dys', ajout_dys, name='dys'),
    path('csv', export_csv, name='csv'),
    path('table', table, name="table"),

]
# Serving the media files in development mode
if settings.DEBUG and not settings.USE_ORACLE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
