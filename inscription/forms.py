from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import FormActions, InlineField, FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset, Layout, Submit, Field
from .models import BaseEleve, Allergie, TroubleCognitif, Spe
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
                    InlineField("prenom_name", wrapper_class='col'),
                    InlineField("nom__icontains", wrapper_class='col'),
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
    # mail de confirmation
    confirmation_email = forms.EmailField(label="Confirmation de l'email", required=False)

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
        self.helper.use_custom_control = True
        # Liste des champs du modèle à afficher
        self.helper.layout = Layout(
            'civility',
            'genre',
            'nom',
            'prenom',
            'nom_usage',
            'pays_naissance',
            'ville_natale',
            'departement_naissance',
            'commune_naissance',
            'date_naissance',
            'nationalite',
            'address',
            'telephone',
            'photo',
            'email',
            'confirmation_email',
        )

    def clean(self):
        """Fonction pour contrôler les entrées"""
        nom = self.cleaned_data['nom']
        prenom = self.cleaned_data['prenom']
        # On vérifie que le couple Nom/Prénom n'est pas déjà dans la base
        check = BaseEleve.objects.filter(nom=nom).filter(prenom=prenom)
        # On exlut l'entrée en cours de cette recherche pour permettre les updates
        if self.instance:
            check = check.exclude(id=self.instance.id)
        # On affiche le message d'erreur
        if check.exists():
            msg = "{} {} est déjà dans la base.".format(nom, prenom)
            self.add_error('nom', msg)
            self.add_error('prenom', msg)
        # On s'assure que le champs ville_natale ou communes et département sont remplis
        msg = forms.ValidationError("Veuillez renseigner ce champs SVP.")
        if self.cleaned_data.get('pays_naissance').name == 'FRANCE':
            self.cleaned_data['ville_natale'] = None
            if self.cleaned_data.get('departement_naissance', None) is None:
                self.add_error('departement_naissance', msg)
                if self.cleaned_data.get('commune_naissance', None) is None:
                    self.add_error('commune_naissance', msg)
                return
            if self.cleaned_data.get('commune_naissance', None) is None:
                self.add_error('commune_naissance', msg)
                return
        else:
            self.cleaned_data['commune_naissance'] = None
            self.cleaned_data['departement_naissance'] = None
            if self.cleaned_data.get('ville_natale', None) is None:
                self.add_error('ville_natale', msg)
                return
        return self.cleaned_data

    def clean_confirmation_mail(self):
        """
        Méthode pour vérifier que le mail correspond bien au
        mail de confirmation lors de la validation du formulaire
        """
        confirmation_email = self.cleaned_data['confirmation_email']
        mail = self.cleaned_data['email']
        # Si l'instance (model) a déjà une ID c'est à dire que c'est un Update d'une entrée existante
        if self.instance.id:
            # On vérifie juste que l'email n'a pas été changé
            if mail == self.instance.email:
                return confirmation_email
        # Si c'est une nouvelle entrée ou si l'email à changé, on compare l'email et la confirmation
        if mail != confirmation_email:
            raise forms.ValidationError(
                "Le mail et le mail de confirmation ne sont pas identiques")
        return confirmation_email

    class Meta:
        # Modèle utilisé et entrées à renseigner
        model = BaseEleve
        fields = ['address', 'civility', 'genre', 'nom', 'prenom', 'nom_usage', 'date_naissance', 'pays_naissance',
                  'photo', 'commune_naissance', 'departement_naissance', 'telephone', 'email', 'confirmation_email',
                  'nationalite', 'ville_natale',]
        # Ajout d'un date picker au format='%Y-%m-%d' pour qu'il affiche les valeurs initiales lors des update
        # https://stackoverflow.com/questions/58294769/django-forms-dateinput-not-populating-from-instance
        widgets = {
            'photo': forms.widgets.FileInput(),
            'date_naissance': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'commune_naissance': autocomplete.ModelSelect2(url='commune',
                                                           forward=('departement_naissance',)),
            'departement_naissance': autocomplete.ModelSelect2(url='departement'),
            'pays_naissance': autocomplete.ModelSelect2(url='pays'),
            'nationalite': autocomplete.ModelSelect2(url='pays'),

        }

    class Media:
        css = {
            'screen': ('css/custom-dark.css',),
        }
        js = (
            'js/form1.js',
        )


class InscriptionForm2(forms.ModelForm):
    name = 'Responsables légaux'

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
            Fieldset("Responsable 1",
                'resp1', 'nom_resp1', 'prenom_resp1', 'adresse_resp1', 'tel_resp1', 'email_resp1', 'sociopro_resp1'
                     ),
            Fieldset("Responsable 2",
                'resp2', 'nom_resp2', 'prenom_resp2', 'adresse_resp2', 'tel_resp2', 'email_resp2','sociopro_resp2'
                     ),
        )

    def clean(self):
        resp2 = self.cleaned_data.get('resp2')
        required = ['nom_resp2', 'prenom_resp2', 'adresse_resp2', 'tel_resp2', 'email_resp2',
                    'sociopro_resp2']
        if resp2 == 'aucun':
            for field in required:
                self.cleaned_data[field] = None
                return
        else:
            msg = forms.ValidationError("Veuillez renseigner ce champs SVP.")
            for field in required:
                if self.cleaned_data.get(field) is None:
                    self.add_error(field, msg)
        return self.cleaned_data

    class Meta:
        # Modèle utilisé et entrées à renseigner
        model = BaseEleve
        fields = ['nom_resp1', 'prenom_resp1', 'nom_resp2', 'prenom_resp2', 'adresse_resp1', 'adresse_resp2',
                  'tel_resp1', 'tel_resp2', 'email_resp1', 'email_resp2', 'sociopro_resp1', 'sociopro_resp2',
                  'resp1', 'resp2', ]

    class Media:
        js = ('js/hide_resp2.js',)
        css = {
            'screen': ('css/custom-dark.css',),
        }


class InscriptionForm3(forms.ModelForm):
    name = 'Scolarité'
    ajout_allergie = forms.CharField(label="Ajouter une allergie", required=False)
    allergie = forms.ModelMultipleChoiceField(
        queryset=Allergie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Allergies"
    )
    dys = forms.ModelMultipleChoiceField(
        queryset=TroubleCognitif.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Troubles de l'apprentissage"
    )
    ajout_dys = forms.CharField(label="Ajouter un trouble", required=False)
    nouvelle = forms.BooleanField(label="Première inscription au LXP", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Id et classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'BaseEleve-form'
        # Largeur des labels et des champs sur la grille
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8 d-flex flex-wrap justify-content-between'
        self.helper.use_custom_control = True
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Field('dys', id='dys'),
            FieldWithButtons('ajout_dys', StrictButton('Enregistrer', id='dys-btn', css_class='btn-outline-success',
                                                       onclick="ajoutDys()")),
            Field('allergie', id='allergie'),
            FieldWithButtons('ajout_allergie', StrictButton('Enregistrer', id='allergie-btn', css_class='btn-outline-success',
                                                                                    onclick="ajoutAllergie()")),
            Field('nouvelle', id='nouvelle', wrapper_class="custom-control custom-switch custom-switch-lg",
                  template='inscription/custom-field.html'),
            'niveau_an_passe',
            'gb_an_passe',
            'ecco_an_passe',
        )

    class Media:
        js = ('js/hide_lxp_an_passe.js',)
        css = {
            'screen': ('css/custom-dark.css',),
        }

    class Meta:
        # Définis le modèle utilisé et des données à enregistrer
        model = BaseEleve
        fields = ['allergie', 'dys', 'nouvelle',  'niveau_an_passe', 'gb_an_passe', 'ecco_an_passe']
        widgets = {
            'ecco_an_passe': autocomplete.ModelSelect2(url='mee',
                                                           forward=('gb_an_passe',)),
        }

    def clean(self):
        nouvelle = self.cleaned_data.get('nouvelle')
        if nouvelle:
            self.cleaned_data['ecco_an_passe'] = None
            self.cleaned_data['gb_an_passe'] = None
            self.cleaned_data['niveau_an_passe'] = None
        else:
            if not self.cleaned_data.get('ecco_an_passe'):
                msg = forms.ValidationError("Indique ton MEE de groupe ECCO de l'an passé.")
                self.add_error('ecco_an_passe', msg)
            if not self.cleaned_data.get('gb_an_passe'):
                msg = forms.ValidationError("Indique ton groupe de base de l'an passé.")
                self.add_error('gb_an_passe', msg)
            if not self.cleaned_data.get('niveau_an_passe'):
                msg = forms.ValidationError("Indique le niveau dans lequel tu étais inscrit l'an passé.")
                self.add_error('niveau_an_passe', msg)
        return self.cleaned_data


class InscriptionForm4(forms.ModelForm):
    name = 'Projet au Lycée'
    # Ajout des champs supplémentaires au modèle
    # captcha
    captcha = CaptchaWizardField()
    confirm = forms.BooleanField(label="Je comprends et accepte que mes spécialités aient lieu en même temps",
                                 required=False, widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)

        # FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Id et classe bootstrap de ton formulaire
        #self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'BaseEleve-form'
        # Largeur des labels et des champs sur la grille
        #self.helper.label_class = 'col-md-4'
        #self.helper.field_class = 'col-md-6'
        self.fields['spe1'].label = False
        self.fields['spe2'].label = False
        self.fields['spe3'].label = False
        # Affichage du formulaire
        self.helper.layout = Layout(
            # Liste des champs à afficher dont les champs supplémentaires
            'comments',
            'niveau',
            Fieldset(
                #HTML("""<label>Spécialités</label>"""),
                'Spécialités',
                    Field('spe1', wrapper_class='col-4'),
                    Field('spe2', wrapper_class='col-4'),
                    Field('spe3', wrapper_class='col-4'),
                    css_class='row', css_id='champ-spe'),
            'confirm',
            'captcha',
        )

    def check_spe(self,spes):
        if spes is not None:
            if len(spes) < 2:
                return False
            else:
                list_type = []
                for spe in spes:
                    if Spe.objects.filter(intitule=spe).values_list('type', flat=True).first() is not None:
                        list_type.append(Spe.objects.filter(intitule=spe).values_list('type', flat=True).first())
                for elem in list_type:
                    if list_type.count(elem) > 1:
                        return True
        return False

    def clean(self):
        niveau = self.cleaned_data.get('niveau')
        confirm = self.cleaned_data.get('confirm')
        groupe_spe = ['spe1', 'spe2', 'spe3']
        spe1 = self.cleaned_data.get('spe1')
        spe2 = self.cleaned_data.get('spe2')
        spe3 = self.cleaned_data.get('spe3')
        if niveau == 'crepa' or niveau == 'deter' :
            self.cleaned_data['spe1'] = None
            self.cleaned_data['spe2'] = None
            self.cleaned_data['spe3'] = None
        elif niveau == 'premiere' :
            if len(spe1)+len(spe2)+len(spe3) == 3:
                if len(spe1) ==1 and len(spe2) == 1 and len(spe3) == 1:
                    return self.cleaned_data
                else:
                    for spe in groupe_spe:
                        if self.check_spe(self.cleaned_data.get(spe)):
                            msg = forms.ValidationError("Vous ne pouvez-pas prendre 2 spé du même type (arts et langues).")
                            self.add_error(spe, msg)
                            return
                    if not confirm:
                        msg = forms.ValidationError("Il est fortement déconseillé de choisir 2 spés dans la même colonne. Ces 2 spés auront systématiquement lieux en même temps. Ne faire ce choix qu'après discussion avec un·e membre de l'équipe éducative.")
                        self.fields['confirm'].widget = forms.CheckboxInput()
                        self.fields['confirm'].required = True
                        self.add_error('confirm', msg)
                    else:
                        return self.cleaned_data
            else:
                msg = forms.ValidationError("Vous devez choisir 3 spécialités.")
                self.add_error('spe1', msg)
                self.add_error('spe2', msg)
                self.add_error('spe3', msg)
        else:
            if len(spe1)+len(spe2)+len(spe3) == 2:
                if len(spe1) > 1 or len(spe2) > 1 or len(spe3) > 1:
                    for spe in groupe_spe:
                        if self.check_spe(self.cleaned_data.get(spe)):
                            msg = forms.ValidationError("Vous ne pouvez-pas prendre 2 spé du même type (arts et langues).")
                            self.add_error(spe, msg)
                            return
                    if not confirm:
                        msg = forms.ValidationError("Il est fortement déconseillé de choisir 2 spés dans la même colonne. Ces 2 spés auront systématiquement lieux en même temps. Ne faire ce choix qu'après discussion avec un·e membre de l'équipe éducative.")
                        self.fields['confirm'].widget = forms.CheckboxInput()
                        self.fields['confirm'].required = True
                        self.add_error('confirm', msg)
                else:
                    return self.cleaned_data
            else:
                msg = forms.ValidationError("Vous devez choisir 2 spécialités.")
                self.add_error('spe1', msg)
                self.add_error('spe2', msg)
                self.add_error('spe3', msg)

    class Meta:
        # Définis le modèle utilisé et des données à enregistrer
        model = BaseEleve
        fields = [
            'comments','spe1', 'spe2', 'spe3','niveau',
        ]

    class Media:
        pass
        js = ('js/form4.js',)