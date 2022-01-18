from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import FormActions, InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset, Layout, Submit
from .models import BaseEleve
from .utils import CaptchaWizardField
# Pour l'autocomplétion de la commune en fonction du département choisi
from dal import autocomplete


class ListeEleveForm(FormHelper):
    """
    Formulaire pour faire des recherches dans le tableau
    Voir https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
    """
    form_class = "form-inline"
    form_id = "inscription-search-form"
    form_method = "GET"
    form_tag = True
    html5_required = True
    # form_style = 'inline'
    field_template = 'bootstrap4/layout/inline_field.html'
    layout = Layout(
        Div(
            Fieldset(
                "<span class='fa fa-search'></span> " + str(_("Rechercher des élèves")),
                Div(
                    # les champs à chercher suivi de __filtre avec le nom du filtre déclaré pour chaque champ dans filter.py
                    # InlineField("birth_name__icontains", css_class='form-group col-4'),
                    InlineField("first_name", wrapper_class='col'),
                    InlineField("last_name__icontains", wrapper_class='col'),
                    css_class="row",
                ),
                css_class="col-10 border p-3",
            ),
            FormActions(
                Submit("submit", _("Filtrer")),
                css_class="col-2 text-right align-self-center",
            ),
            css_class="row",
        )
    )


class InscriptionForm1(forms.ModelForm):
    """
    Formulaire d'inscription
    """
    ### Le nom du formulaire, affiché dans le template (wizard.form.name)
    name = 'Identité'

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # FormHelper pour customiser le formulaire
        self.helper = FormHelper()
        # Id et la classe bootstrap du formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'BaseEleve-form'
        # Largeur des labels et des champs sur la grille
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        # Liste des champs du modèle à afficher
        self.helper.layout = Layout(
            'civility',
            'last_name',
            'first_name',
            'departement_naissance',
            'commune_naissance',
            'birth_date',
            'birth_place',
            'birth_country',
            'address',
            'photo',
        )

    def clean(self):
        """Fonction pour contrôler les entrées"""
        last_name = self.cleaned_data['last_name']
        first_name = self.cleaned_data['first_name']
        # On vérifie que le couple Nom/Prénom n'est pas déjà dans la base
        check = BaseEleve.objects.filter(first_name=first_name).filter(last_name=last_name)
        # On exlut l'entrée en cours de cette recherche pour permettre les updates
        if self.instance:
            check = check.exclude(id=self.instance.id)
        # On affiche le message d'erreur
        if check.exists():
            msg = "{} {} est déjà dans la base.".format(first_name, last_name)
            self.add_error('last_name', msg)
            self.add_error('first_name', msg)

    class Meta:
        # Modèle utilisé et entrées à renseigner
        model = BaseEleve
        fields = ['address', 'civility', 'last_name', 'first_name', 'birth_date', 'birth_place', 'birth_country',
                  'photo', 'commune_naissance', 'departement_naissance']
        # Ajout d'un date picker au format='%Y-%m-%d' pour qu'il affiche les valeurs initiales lors des update
        # https://stackoverflow.com/questions/58294769/django-forms-dateinput-not-populating-from-instance
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'commune_naissance': autocomplete.ModelSelect2(url='linked_data',
                                              forward=('departement_naissance',))
        }

    class Media:
        js = (
            'linked_data.js',
        )

class InscriptionForm2(forms.ModelForm):
    name = 'Adresse'

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'BaseEleve-form'
        # Largeur des labels et des champs sur la grille
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        # Affichage de ton formulaire
        self.helper.layout = Layout(
            # Liste des champs à afficher
            'street_number',
            'street_type',
            'street',
            'comp_1',
            'comp_2',
            'city',
            'zip_code',
            'country',
            'phone',
        )

    class Meta:
        # Modèle utilisé et entrées à renseigner
        model = BaseEleve
        fields = ['street_number',
                  'street_type',
                  'street',
                  'comp_1',
                  'comp_2',
                  'city',
                  'zip_code',
                  'country',
                  'phone', ]


class InscriptionForm3(forms.ModelForm):
    name = 'Validation'
    # Ajout des champs supplémentaires au modèle
    # captcha
    captcha = CaptchaWizardField()
    # mail de confirmation
    confirmation_mail = forms.EmailField(label="Mail de confirmation", required=False)

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)

        # FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Id et classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'BaseEleve-form'
        # Largeur des labels et des champs sur la grille
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-6'
        # Affichage du formulaire
        self.helper.layout = Layout(
            # Liste des champs à afficher dont les champs supplémentaires
            'mail',
            'confirmation_mail',
            'comments',
            'captcha',
        )

    def clean_confirmation_mail(self):
        """
        Méthode pour vérifier que le mail correspond bien au
        mail de confirmation lors de la validation du formulaire
        """
        confirmation_mail = self.cleaned_data['confirmation_mail']
        mail = self.cleaned_data['mail']
        # Si l'instance (model) a déjà une ID c'est à dire que c'est un Update d'une entrée existante
        if self.instance.id:
            # On vérifie juste que l'email n'a pas été changé
            if mail == self.instance.mail:
                return confirmation_mail
        # Si c'est une nouvelle entrée ou si l'email à changé, on compare l'email et la confirmation
        if mail != confirmation_mail:
            raise forms.ValidationError(
                "Le mail et le mail de confirmation ne sont pas identiques")
        return confirmation_mail

    class Meta:
        # Définis le modèle utilisé et des données à enregistrer
        model = BaseEleve
        fields = [
            'mail',
            'comments',
        ]
