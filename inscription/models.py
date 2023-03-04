from django.db import models
from address.models import AddressField
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from .utils import nom_photo, create_hash

GB = (
    ('G1', 'G1'),
    ('G2', 'G2'),
    ('G3', 'G3'),
    ('G4', 'G4'),
    ('G5', 'G5'),
)

class LVManager(models.Manager):
    def get_by_natural_key(self, langue):
        return self.get(langue=langue)


class LV(models.Model):
    langue = models.CharField(max_length=10, verbose_name="Langue", unique=True)
    siecle = models.CharField(max_length=2, verbose_name="Code Siecle")
    cyclades = models.CharField(max_length=10, verbose_name="Code Cyclades")
    objects = LVManager()

    def natural_key(self):
        return [self.langue]

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s' % self.langue


class SpeManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Spe(models.Model):
    code = models.CharField(max_length=10, verbose_name="Code Spé", unique=True)
    intitule = models.CharField(max_length=50, verbose_name="Intitulé Spé")
    groupe = models.CharField(max_length=2, verbose_name="Groupe Spé", null=True, blank=True)
    type = models.CharField(max_length=10, verbose_name="Type Spé", null=True, blank=True)
    objects = SpeManager()

    def natural_key(self):
        return [self.code]

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s' % self.intitule


class SocioproManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Sociopro(models.Model):
    """Base de donnée des codes socioprofessionnels.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py sociopro"""
    code = models.CharField(max_length=4, verbose_name="Code Sociopro", unique=True)
    name = models.CharField(max_length=100, verbose_name="Catégorie sociopro")
    objects = SocioproManager()

    def natural_key(self):
        return [self.code]

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s' % self.name


class PaysManager(models.Manager):
    def get_by_natural_key(self, code, name):
        return self.get(code=code, name=name)


class Pays(models.Model):
    """Base de donnée des pays avec code INSEE.
    Les données sont importées depuis le fichier CSV grâce à la commande python manage.py pays"""
    code = models.CharField(max_length=4, verbose_name="Code INSEE")
    name = models.CharField(max_length=50, verbose_name="Département")
    objects = PaysManager()

    def natural_key(self):
        return [self.code, self.name]

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s' % (self.name)

    class Meta:
        unique_together = ('code', 'name',)


class DepartementManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Departement(models.Model):
    """Base de donnée des départements avec code INSEE.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py departement"""
    code = models.CharField(max_length=4, verbose_name="Code INSEE", unique=True)
    name = models.CharField(max_length=50, verbose_name="Département")
    objects = DepartementManager()

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s - %s' % (self.code, self.name)

    def natural_key(self):
        return [self.code]


class CommuneManager(models.Manager):
    def get_by_natural_key(self, code, name):
        return self.get(code=code, name=name)


class Commune(models.Model):
    """Base de donnée des communes avec code INSEE et département d'appartenance.
    Les données sont importées depuis le fichier CSV grâce à la commande python manage.py commune"""
    code = models.CharField(max_length=6, verbose_name="Code INSEE")
    name = models.CharField(max_length=50, verbose_name="Commune")
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département", to_field='code')
    objects = CommuneManager()

    def natural_key(self):
        return [self.code, self.name]

    class Meta:
        unique_together = [['code', 'name']]

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return u'%s' % (self.name)


class TroubleManager(models.Manager):
    def get_by_natural_key(self, trouble):
        return self.get(trouble=trouble)


class TroubleCognitif(models.Model):
    trouble = models.CharField(max_length=100, unique=True)
    objects = TroubleManager()

    def natural_key(self):
        return [self.trouble]

    def __str__(self):
        return '%s' % self.trouble


class AllergieManager(models.Manager):
    def get_by_natural_key(self, allergene):
        return self.get(allergene=allergene)


class Allergie(models.Model):
    allergene = models.CharField(max_length=100, unique=True)
    objects = AllergieManager()

    def natural_key(self):
        return [self.allergene]

    def __str__(self):
        return '%s' % self.allergene


class MeeManager(models.Manager):
    def get_by_natural_key(self, prenom):
        return self.get(prenom=prenom)


class MEE(models.Model):
    # nom = models.CharField(max_length=20, verbose_name="Nom")
    prenom = models.CharField(max_length=20, verbose_name="Prénom", unique=True)
    gb = models.JSONField(default=dict)
    gb_an_passe = models.IntegerField(choices=GB,
                                      verbose_name="GB de l'an passé", blank=True, null=True)
    gb_annee_en_cours = models.IntegerField(choices=GB,
                                            verbose_name="GB de cette année", blank=True, null=True)
    # email = models.EmailField(verbose_name="Email", max_length=30,  blank=True, null=True)
    # telephone = PhoneNumberField(verbose_name="Téléphone",  blank=True, null=True)
    objects = MeeManager()

    def natural_key(self):
        #    return [self.prenom, self.nom]
        return self.prenom

    def __str__(self):
        return '%s' % self.prenom
    # class Meta:
    #    unique_together = [['prenom', 'nom']]


class Etablissement(models.Model):
    nom_commune = models.CharField(max_length=50, null=True)
    code_commune = models.CharField(max_length=6, null=True)
    # commune = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune", null=True)
    appartenance_education_prioritaire = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True, )
    code_nature = models.IntegerField(null=True)
    nombre_d_eleves = models.CharField(max_length=50, null=True, blank=True)
    type_etablissement = models.CharField(max_length=50, null=True)
    libelle_nature = models.CharField(max_length=50, null=True)
    nom_etablissement = models.CharField(max_length=150, null=True)
    identifiant_de_l_etablissement = models.CharField(max_length=10, null=True)
    statut_public_prive = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '%s - %s' % (self.nom_etablissement, self.nom_commune)
    # section_europeenne  = models.CharField(max_length=50, null=True, blank=True)
    # lycee_militaire = models.CharField(max_length=50, null=True, blank=True)
    # voie_generale= models.CharField(max_length=50, null=True, blank=True)
    # voie_professionnelle = models.CharField(max_length=50, null=True, blank=True)
    # section_arts = models.CharField(max_length=50, null=True, blank=True)
    # lycee_agricole = models.CharField(max_length=50, null=True, blank=True)
    # section_internationale =  models.CharField(max_length=50, null=True, blank=True)
    # post_bac =  models.CharField(max_length=50, null=True, blank=True)
    # section_cinema =  models.CharField(max_length=50, null=True, blank=True)
    # apprentissage  =  models.CharField(max_length=50, null=True, blank=True)
    # section_theatre =  models.CharField(max_length=50, null=True, blank=True)
    # voie_technologique =  models.CharField(max_length=50, null=True, blank=True)
    # section_sport =  models.CharField(max_length=50, null=True, blank=True)
    # fiche_onisep =  models.CharField(max_length=50, null=True, blank=True)
    # fax  =  models.CharField(max_length=50, null=True, blank=True)
    # web =  models.CharField(max_length=50, null=True, blank=True)
    # code_region = models.CharField(max_length=3, verbose_name="Région")
    # nom_circonscription =  models.CharField(max_length=50, null=True, blank=True)
    # pial = models.CharField(max_length=10, null=True)
    # adresse_1 = models.CharField(max_length=50, null=True)
    # adresse_2 =  models.CharField(max_length=50, null=True, blank=True)
    # libelle_zone_animation_pedagogique = models.CharField(max_length=10, null=True)
    # adresse_3 = models.CharField(max_length=50, null=True)
    # code_type_contrat_prive = models.CharField(max_length=5, null=True)
    # code_departement = models.CharField(max_length=5, null=True)
    # libelle_region = models.CharField(max_length=50, null=True)
    # precision_localisation = models.CharField(max_length=50, null=True)
    # type_contrat_prive = models.CharField(max_length=50, null=True)
    # code_academie = models.CharField(max_length=5, null=True)
    # ulis = models.BooleanField(null=True)
    # greta = models.CharField(max_length=5)
    # siren_siret = models.CharField(max_length=20, null=True)
    # telephone = models.CharField(max_length=20, null=True)
    # position = models.CharField(max_length=100, null=True)
    # coordy_origine = models.FloatField(null=True)
    # etat = models.CharField(max_length=20, null=True)
    # ministere_tutelle = models.CharField(max_length=50, null=True)
    # code_zone_animation_pedagogique = models.CharField(max_length=20, null=True)
    # coordx_origine = models.FloatField(null=True)
    # lycee_des_metiers = models.CharField(max_length=1, null=True)
    # libelle_departement = models.CharField(max_length=20, null=True)
    # hebergement = models.CharField(max_length=1, null=True)
    # segpa = models.CharField(max_length=1, null=True)
    # restauration = models.BooleanField(null=True)
    # multi_uai = models.BooleanField(null=True)
    # code_postal = models.CharField(max_length=10, null=True)
    # libelle_academie = models.CharField(max_length=20, null=True)
    # date_maj_ligne = models.DateField(null=True)
    # rpi_concentre = models.BooleanField(null=True)
    # epsg_origine = models.CharField(max_length=20, null=True)
    # date_ouverture = models.DateField(null=True)
    # mail = models.CharField(max_length=50, null=True)
    # type_rattachement_etablissement_mere = models.CharField(max_length=50, null=True, blank=True)
    # etablissement_mere = models.CharField(max_length=50, null=True, blank=True)


class BaseEleve(models.Model):
    """
    Modèle de base de donnée BaseEleve
    On définit une manière d'itérer le modèle pour faciliter son affichage dans un template
    # https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
    J'ai remplacé value_to_string par value_from_object pour filtrer la date dans le template : if val.year ...
    """

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_from_object(self)

    CIVILITY_CHOICES = (
        ('M.', 'M.'),
        ('MME', 'Mme')
    )

    GENRE = (
        ('il', 'Il'),
        ('elle', 'Elle'),
        ('iel', 'Il, Elle, Iel ou autre')
    )
    RESP1 = (
        ('pere', 'Père'),
        ('mere', 'Mère'),
        ('autre', 'Autre responsable légal ou référent'),
    )
    RESP2 = (
        ('pere', 'Père'),
        ('mere', 'Mère'),
        ('autre', 'Autre responsable légal ou référent·e'),
        ('aucun', "Pas d'autre référent·e")
    )
    NIVEAU_AN_PASSE = (
        ('3eme', 'Troisième'),
        ('deter', 'Détermination (2nde)'),
        ('premiere', 'Première'),
        ('term', 'Terminale'),
        ('crepa', 'CREPA'),
        ('autre', 'Autre')
    )
    NIVEAU = (
        ('deter', 'Détermination (2nde)'),
        ('premiere', 'Première'),
        ('term', 'Terminale'),
        ('crepa', 'CREPA'),
    )
    date_naissance = models.DateField(verbose_name="Date de naissance")
    commune_naissance = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune de naissance",
                                          blank=True, null=True)
    ville_naissance_etrangere = models.CharField(max_length=50, verbose_name="Ville natale", blank=True, null=True)
    depCOM_naissance = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département de naissance",
                                         blank=True, null=True)
    pays_naissance = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Pays de naissance")
    nationalite = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Nationalité",
                                    related_name='nationalite')
    address = AddressField(verbose_name="Adresse", related_name='eleve', blank=True, null=True,
                           help_text="Si tu n'as pas encore d'addresse dans les environs de Saint-Nazaire, laisse ce champ vide.")

    civilite = models.CharField(max_length=3, choices=CIVILITY_CHOICES, default='MME', verbose_name="Civilité",
                                help_text="Quel sexe t'est attribué dans les documents administratifs ?")
    genre = models.CharField(max_length=5, choices=GENRE, verbose_name='Pronom', default='elle',
                             help_text="Veux-tu que l'on parle de toi en disant il, elle, iel ou autre ?")
    nom_famille = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenoms = models.CharField(max_length=255, verbose_name="Prénom")
    prenom_usage = models.CharField(max_length=255, verbose_name="Prénom d'usage", blank=True, null=True,
                                    help_text="Souhaites-tu être appelé autrement que par ton prénom administratif ?")
    adresse_mail = models.EmailField(max_length=255, verbose_name="Email",
                                     help_text="Prends le temps de te créer une adresse email si tu n'en as pas encore.")
    telephone_mobile = PhoneNumberField(verbose_name="Téléphone")
    projet = models.TextField(verbose_name="Projet au LXP",
                              help_text="Détaille ici ton projet : pourquoi faire le choix du Lycée Expérimental ?")

    hash = models.CharField(max_length=30, default=create_hash, unique=True)
    photo = models.ImageField(upload_to=nom_photo, blank=True, null=True,
                              help_text="Merci de téléverser une photo pour ta fiche d'inscription.")
    # RESPONSABLES

    resp1 = models.CharField(max_length=5, choices=RESP1,
                             default='mere', verbose_name="Lien de parenté ou autre")
    civilite_resp1 = models.CharField(max_length=3, choices=CIVILITY_CHOICES, default='M.', verbose_name="Civilité")
    nom_resp1 = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom_resp1 = models.CharField(max_length=255, verbose_name="Prénom")
    adresse_resp1 = AddressField(verbose_name="Adresse", related_name='resp1')
    email_resp1 = models.EmailField(max_length=255, verbose_name="Email")
    tel_resp1 = PhoneNumberField(verbose_name="Numéro de téléphone")
    sociopro_resp1 = models.ForeignKey(Sociopro, related_name='resp1',
                                       on_delete=models.CASCADE, verbose_name="Profession")
    resp2 = models.CharField(max_length=5, choices=RESP2,
                             default='pere', verbose_name="Lien de parenté")
    civilite_resp2 = models.CharField(max_length=3, choices=CIVILITY_CHOICES, default='M.', verbose_name="Civilité",
                                      blank=True, null=True)
    nom_resp2 = models.CharField(max_length=255, verbose_name="Nom de famille", blank=True, null=True)
    prenom_resp2 = models.CharField(max_length=255, verbose_name="Prénom", blank=True, null=True)
    adresse_resp2 = AddressField(verbose_name="Adresse", related_name='resp2', blank=True, null=True)
    email_resp2 = models.EmailField(max_length=255, verbose_name="Email", blank=True, null=True)
    tel_resp2 = PhoneNumberField(verbose_name="Numéro de téléphone", blank=True, null=True)
    sociopro_resp2 = models.ForeignKey(Sociopro, related_name='resp2',
                                       on_delete=models.CASCADE, verbose_name="Profession", blank=True, null=True)
    spes = models.ManyToManyField(Spe, null=True, blank=True, related_name='spes')
    spe1 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '1'}, null=True, blank=True, related_name='spe1')
    spe2 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '2'}, null=True, blank=True, related_name='spe2')
    spe3 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '3'}, null=True, blank=True, related_name='spe3')

    lv1 = models.ForeignKey(LV, related_name='lv1',
                                       on_delete=models.CASCADE, verbose_name="Première langue vivante")
    lv2 = models.ForeignKey(LV, related_name='lv2',
                            on_delete=models.CASCADE, verbose_name="Deuxième langue vivante")
    niveau = models.CharField(max_length=10, choices=NIVEAU, verbose_name="Niveau d'inscription", default='deter')
    # Scolarité passée
    troubles = models.ManyToManyField(TroubleCognitif, verbose_name="Troubles de l'apprentissage", blank=True,
                                      null=True,
                                      help_text="As-tu des troubles de l'apprentissage ou une situation médicale impactant ta scolarité ?")

    amenagements = models.BooleanField(verbose_name="Aménagements d'épreuves", default=False,
                                       help_text="As-tu déjà bénéficié d'aménagement d'épreuves pour ces troubles ?")

    allergies = models.ManyToManyField(Allergie, verbose_name="Allergies", blank=True, null=True)

    boursier = models.BooleanField(verbose_name='Bénéficiaire de bourses', default=False,
                                   help_text="Étais-tu boursier·e l'an passé ?")

    desco = models.BooleanField(verbose_name='Déscolarisation', default=False,
                                help_text="Étais-tu déscolarisé·e l'an passé ?")

    ancien = models.BooleanField(verbose_name='Réinscription au LXP', default=False,
                                 help_text="Étais-tu inscrit·e au LXP l'an passé ?")

    date_entretien = models.DateField(verbose_name="Date de ton entretien", blank=True, null=True,
                                      help_text="Indique une date approximative si tu n'as plus la date exacte.")

    mee_entretien = models.ForeignKey(MEE, on_delete=models.CASCADE, related_name='entretien',
                                      verbose_name="MEE d'entretien", blank=True, null=True,
                                      help_text="Laisse vide si tu ne te souviens plus du prénom du/de la MEE que tu as rencontré.")

    niveau_an_passe = models.CharField(max_length=10, choices=NIVEAU_AN_PASSE,
                                       verbose_name="Niveau d'inscription l'an passé", blank=True, null=True)
    gb_an_passe = models.IntegerField(choices=GB,
                                      verbose_name="Groupe de base", blank=True, null=True)
    ecco_an_passe = models.ForeignKey(MEE, on_delete=models.CASCADE, related_name='ecco_an_passe',
                                      verbose_name="MEE d'ECCO", blank=True, null=True)

    gb_annee_en_cours = models.IntegerField(choices=GB,
                                            verbose_name="Groupe de base", blank=True, null=True)

    etablissement_origine = models.ForeignKey(Etablissement, on_delete=models.CASCADE,
                                              verbose_name="Etablissement d'origine", blank=True, null=True,
                                              help_text="Où étiez-vous avant de vous inscrire au Lycée Expérimental ?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)