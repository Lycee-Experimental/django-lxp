from __future__ import unicode_literals

import os

from dal import autocomplete
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils import timezone
# La vue de formulaire Wizard
from formtools.wizard.views import SessionWizardView
# Filtres de recherche dans la base
from djangoLxp import settings
from .filters import ListeEleveFiltre
# Base BaseEleve
from .models import BaseEleve, Pays, Departement, Allergie, TroubleCognitif
# Tableau des inscrits
from .tables import ListeEleveTableau
# Une vue pour afficher les inscriptions filtées
from .utils import PagedFilteredTableView, MediaStorage, coordonnees
# Nos différents formulaires
from .forms import InscriptionForm1, InscriptionForm2, InscriptionForm3, InscriptionForm4, ListeEleveForm
### Librairie weasyprint pour la génération de PDF
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def fiche(request, **kwargs):
    """
    Affichage d'une fiche d'inscription
    """
    id=kwargs['id']
    hash=kwargs['hash']
    eleve = get_object_or_404(BaseEleve, id=id, hash=hash)
    return render(request, 'inscription/fiche_inscription.html', {'fiche': eleve})


# Un décorateur pour authoriser le téléchargement aux utilisateurs authentifiés
# @login_required(login_url='/admin/login/')
def fiche_pdf(request, **kwargs):
    """
        Affichage d'une fiche d'inscription en PDF avec weasyprint
    """
    id=kwargs['id']
    hash=kwargs['hash']
    eleve = get_object_or_404(BaseEleve, id=id, hash=hash)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=fiche-{name}-{date}.pdf".format(
        date=timezone.now().strftime('%Y-%m-%d'),
        name=slugify(eleve.prenom),
    )
    html = render_to_string("inscription/fiche_inscription.html", {
        'fiche': eleve,
    })
    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[
        'https://cdn.jsdelivr.net/npm/bootstrap@4/dist/css/bootstrap.min.css'], font_config=font_config, presentational_hints=True)
    return response


def ajout_allergie(request):
    """Une vue pour ajouter une allergie en jquery depuis le formulaire Wizard"""
    if request.POST:
        p, created = Allergie.objects.get_or_create(
            allergene=request.POST.get('allergene').capitalize(),
        )
        return HttpResponse('success')


def ajout_dys(request):
    """Une vue pour ajouter un trouble en jquery depuis le formulaire Wizard"""
    if request.POST:
        p, created = TroubleCognitif.objects.get_or_create(
            trouble=request.POST.get('trouble').capitalize(),
        )
        return HttpResponse('success')


class FormulaireInscription(SessionWizardView):
    """
    Vue du formulaire wizard (en plusieurs étapes)
    """
    # Liste des formulaires à inclure dans le wizard
    form_list = [InscriptionForm1, InscriptionForm2, InscriptionForm3, InscriptionForm4]
    template_name = 'inscription/formulaire_inscription.html'
    instance = None
    if settings.USE_S3:
        file_storage = MediaStorage(location='tmp')
    else:
        file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

    def get_form_instance(self, step):
        """Connection du wizard à une instance de la base de donnée
        Soit nouvelle, soit existante à partir de l' id envoyé en kwargs, par l'entrée url.py :
        path('update/<int:id>', login_required(FormulaireInscription.as_view(form_list)), name='update'),
        """
        if self.instance is None:
            # Si id existant (update)
            if 'id' in self.kwargs:
                id = self.kwargs['id']
                hash = self.kwargs['hash']
                self.instance = BaseEleve.objects.get(id=id, hash=hash)
            # Sinon, nouvelle instance d'BaseEleve
            else:
                self.instance = BaseEleve()
        return self.instance

    def done(self, form_list, **kwargs):
        # On sauvegarde les données
        self.instance.save()
        # On redirige vers le PDF
        url = reverse('inscription:pdf', kwargs={'id': self.instance.id, 'hash': self.instance.hash})
        return HttpResponseRedirect(url)


class InscriptionView(PagedFilteredTableView):
    """ Une view pour afficher un tableau de recherche dans la base.
    """
    filter_class = ListeEleveFiltre
    model = BaseEleve
    table_class = ListeEleveTableau
    template_name = "inscription/filtre_eleves.html"
    formhelper_class = ListeEleveForm

    def get_queryset(self):
        return BaseEleve.objects.filter()


def carto(request, **kwargs):
    """
    Affichage de la carte des adresses
    """
    return render(request, 'inscription/carto.html', {'adresses': coordonnees(BaseEleve.objects.all())})


class AutocompleteCommune(autocomplete.Select2QuerySetView):
    """Une vue pour permettre l'autocomplétion de recherche de commune par département."""
    def get_queryset(self):
        qs = super(AutocompleteCommune, self).get_queryset()
        dep = self.forwarded.get('departement_naissance', None)

        if dep:
            qs = qs.filter(departement_id=dep)
        return qs


class AutocompleteDepartement(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Departement.objects.all().order_by('code')
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q)|Q(code__icontains=self.q))
        return qs


class AutocompletePays(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pays.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs