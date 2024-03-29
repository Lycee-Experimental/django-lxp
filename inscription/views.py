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
from .models import BaseEleve, Pays, Departement, Allergie, TroubleCognitif, MEE, Etablissement
from .tables import ListeEleveTableau
# Une vue pour afficher les inscriptions filtées
from .utils import PagedFilteredTableView, MediaStorage, coordonnees
# Nos différents formulaires
from .forms import InscriptionForm1, InscriptionForm2, InscriptionForm3, InscriptionForm4, ListeEleveForm
### Librairie weasyprint pour la génération de PDF
from .utils import download_csv, generate_pdf
from ajax_datatable.views import AjaxDatatableView


def validation(request, **kwargs):
    """
    Page de téléchargement de la fiche d'inscription
    """
    id=kwargs['id']
    hash=kwargs['hash']
    eleve = get_object_or_404(BaseEleve, id=id, hash=hash)
    return render(request, 'inscription/validation.html', {'fiche': eleve})


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
    id=kwargs['id']
    hash=kwargs['hash']
    eleve = get_object_or_404(BaseEleve, id=id, hash=hash)
    html = render_to_string("inscription/fiche_inscription.html",
                            {'fiche': eleve,}, request=request)
    pdf=generate_pdf(html)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=fiche-{name}-{date}.pdf".format(
        date=timezone.now().strftime('%Y-%m-%d'),
        name=slugify(eleve.prenoms),
    )
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
    if settings.USE_ORACLE:
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
        form_data = [form.cleaned_data for form in form_list]
        for value in form_data[3]['spe1'] or []:
            self.instance.spe1.add(value)
        for value in form_data[3]['spe2'] or []:
            self.instance.spe2.add(value)  
        for value in form_data[3]['spe3'] or []:
            self.instance.spe3.add(value)  
        #form_data_dict = self.get_all_cleaned_data()
        #Nécessaire de sauvegarder les manyToMany différemment
        #spe_values = form_data_dict.pop('spe')
        #for value in form_data_dict.pop('dys'):
        #    self.instance.dys.add(value)
        #for value in form_data_dict.pop('allergie'):
        #    self.instance.allergie.add(value)
        #for value in form_data_dict.pop('spe1'):
        #    self.instance.spe1.add(value)
        #for value in form_data_dict.pop('spe2'):
        #    self.instance.spe2.add(value)  
        #for value in form_data_dict.pop('spe3'):
        #    self.instance.spe3.add(value)         
        ## On redirige vers le PDF
        #url = reverse('inscription:pdf', kwargs={'id': self.instance.id, 'hash': self.instance.hash})
        url = reverse('inscription:validation', kwargs={'id': self.instance.id, 'hash': self.instance.hash})
        return HttpResponseRedirect(url)





class InscriptionRechercheView(PagedFilteredTableView):
    """ Une view pour afficher un tableau de recherche dans la base.
    """
    filter_class = ListeEleveFiltre
    model = BaseEleve
    table_class = ListeEleveTableau
    template_name = "inscription/recherche_eleves.html"
    formhelper_class = ListeEleveForm

    def get_queryset(self):
        return BaseEleve.objects.filter()


class InscriptionTableView(PagedFilteredTableView):
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
        dep = self.forwarded.get('depCOM_naissance', None)
        code = Departement.objects.get(id=dep).code
        if dep:
            qs = qs.filter(departement_id=code)
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


class AutocompleteMEE(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MEE.objects.all().order_by('prenom')
        gb = self.forwarded.get('gb_an_passe', None)
        annee = self.forwarded.get('annee', '2023')
        if gb:
            qs = qs.filter(gb__contains={annee: int(gb)})
        if self.q:
            qs = qs.filter(prenom__istartswith=self.q)
        return qs


class AutocompleteEtablissement(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Etablissement.objects.all().order_by('nom_etablissement')
        if self.q:
            qs = qs.filter(Q(nom_etablissement__icontains=self.q)|Q(nom_commune__icontains=self.q))
        return qs


class AutocompleteAllergie(autocomplete.Select2QuerySetView):
    create_field = 'allergene'    # Pour créer une entrée si non trouvée

    def has_add_permission(self, request):
        """On redéfinit cette fonction pour que n'importe qui puisse créer une nouvelle entrée"""
        return True

    def get_queryset(self):
        qs = Allergie.objects.all().order_by('allergene')
        if self.q:
            qs = qs.filter(allergene__icontains=self.q)
        return qs

class AutocompleteDys(autocomplete.Select2QuerySetView):
    create_field = 'trouble'    # On indique le champs à créer si non trouvé
    def has_add_permission(self, request):
        """On redéfinit cette fonction pour que n'importe qui puisse créer une nouvelle entrée"""
        return True

    def get_queryset(self):
        qs = TroubleCognitif.objects.all().order_by('trouble')
        if self.q:
            qs = qs.filter(trouble__icontains=self.q)
        return qs


## Pour télécharger un csv
def export_csv(request):
  # Create the HttpResponse object with the appropriate CSV header.
  data = download_csv(request, BaseEleve.objects.exclude(address=None))
  response = HttpResponse(data, content_type='text/csv')
  return response


class ElevesAjaxDatatableView(AjaxDatatableView):
    model = BaseEleve
    title = 'Eleves'
    initial_order = [["nom_famille", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, }, #quand même visible à l'export pdf
        {'name': 'nom_famille', 'visible': True, },
        {'name': 'prenom_usage', 'visible': True, },
        {'name': 'genre', 'visible': False, },
        {'name': 'prenoms', 'visible': True, },
        {'name': 'telephone_mobile', 'visible': True, },
        {'name': 'niveau', 'visible': True, },
        {'name': 'adresse_mail', 'visible': False, },
        {'name': 'address',  'foreign_field': 'address__locality__state__name', 'visible': True, },
        {'name': 'spe1', 'm2m_foreign_field': 'spe1__intitule', 'visible': False, },
        {'name': 'spe2', 'm2m_foreign_field': 'spe2__intitule', 'visible': False, },
        {'name': 'spe3', 'm2m_foreign_field': 'spe3__intitule', 'visible': False, },
        {'name': 'lv1', 'visible': False, },
        {'name': 'lv2', 'visible': False, },
    ]

def table(request, **kwargs):
    """
    Page de téléchargement de la fiche d'inscription
    """
    return render(request, 'inscription/datatable.html')
