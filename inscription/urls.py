from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import InscriptionView, FormulaireInscription, form_list, fiche, fiche_pdf, carto

app_name = 'inscription'

urlpatterns = [
    path('inscriptions', login_required(InscriptionView.as_view()), name="inscriptions"),
    path('', FormulaireInscription.as_view(form_list), name='formulaire'),
    path('<int:id>/<hash>', FormulaireInscription.as_view(form_list), name='update'),
    path('fiche/<int:id>/<hash>', fiche, name='fiche'),
    path('pdf/<int:id>/<hash>', fiche_pdf, name='pdf'),
    path('carto', carto, name='carto'),
]

# Serving the media files in development mode
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#else:
urlpatterns += staticfiles_urlpatterns()