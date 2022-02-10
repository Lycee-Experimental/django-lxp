from django.db import models
from address.models import AddressField
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from .utils import nom_photo, create_hash

GB = (
    (1, 'G1'),
    (2, 'G2'),
    (3, 'G3'),
    (4, 'G4'),
    (5, 'G5'),
)

class Spe(models.Model):
    code = models.CharField(max_length=10, verbose_name="Code Spé")
    intitule = models.CharField(max_length=50, verbose_name="Intitulé Spé")
    groupe = models.CharField(max_length=2, verbose_name="Groupe Spé", null=True, blank=True)
    type = models.CharField(max_length=10, verbose_name="Type Spé", null=True, blank=True)

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return  u'%s' % self.intitule


class Sociopro(models.Model):
    """Base de donnée des codes socioprofessionnels.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py sociopro"""
    code = models.CharField(max_length=4, verbose_name="Code Sociopro")
    name = models.CharField(max_length=100, verbose_name="Catégorie sociopro")

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return  u'%s' % self.name


class Pays(models.Model):
    """Base de donnée des pays avec code INSEE.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py pays"""
    code = models.CharField(max_length=4, verbose_name="Code INSEE")
    name = models.CharField(max_length=50, verbose_name="Département")

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return  u'%s' % (self.name)


class Departement(models.Model):
    """Base de donnée des départements avec code INSEE.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py departement"""
    code = models.CharField(max_length=4, verbose_name="Code INSEE")
    name = models.CharField(max_length=50, verbose_name="Département")

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return  u'%s - %s' % (self.code, self.name)


class Commune(models.Model):
    """Base de donnée des communes avec code INSEE et département d'appartenance.
    Le données sont importées depuis le fichier CSV grâce à la commande python manage.py commune"""
    code = models.CharField(max_length=6, verbose_name="Code INSEE")
    name = models.CharField(max_length=50, verbose_name="Commune")
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département")

    def __str__(self):
        """Indique ce que donne l'affichage de la classe, notamment dans les menus déroulants"""
        return  u'%s' % (self.name)


class TroubleCognitif(models.Model):
    trouble = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.trouble


class Allergie(models.Model):
    allergene = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.allergene


class MEE(models.Model):
    nom = models.CharField(max_length=20, verbose_name="Nom")
    prenom = models.CharField(max_length=20, verbose_name="Prénom")
    gb_an_passe = models.IntegerField(choices=GB,
                                      verbose_name="GB de l'an passé", blank=True, null=True)
    gb_annee_en_cours = models.IntegerField(choices=GB,
                                            verbose_name="GB de cette année", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", max_length=30,  blank=True, null=True)
    telephone = PhoneNumberField(verbose_name="Téléphone",  blank=True, null=True)

    def __str__(self):
        return '%s' % self.prenom


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
        ('il', 'il'),
        ('elle', 'elle'),
        ('iel', 'iel')
    )

    date_naissance = models.DateField(verbose_name="Date de naissance")
    commune_naissance = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune de naissance",
                                          blank=True, null=True)
    ville_natale = models.CharField(max_length=50, verbose_name="Ville natale",blank=True, null=True)
    departement_naissance = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département de naissance", blank=True, null=True)
    pays_naissance = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Pays de naissance")
    nationalite = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Nationalité", related_name='nationalite',)
    address = AddressField(verbose_name="Adresse", related_name='eleve')
    civility = models.CharField(max_length=3, choices=CIVILITY_CHOICES, default='M.', verbose_name="Civilité",
                                help_text="Quel sexe t'est attribué dans les documents administratifs ?")
    genre = models.CharField(max_length=5, choices=GENRE, verbose_name='Pronom', default='Iel',
                             help_text="Veux-tu que l'on parle de toi en disant il, elle ou iel ?")
    nom = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    nom_usage = models.CharField(max_length=255, verbose_name="Nom d'usage", blank=True, null=True,
        help_text="Souhaites-tu être appelé par un nom différent de ton prénom ?")
    email = models.EmailField(max_length=255, verbose_name="Email")
    telephone = PhoneNumberField(verbose_name="Téléphone")
    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    hash = models.CharField(max_length=30, default=create_hash, unique=True)
    photo = models.ImageField(upload_to=nom_photo, null=True)
    # RESPONSABLES
    RESP1 = (
        ('pere','Père'),
        ('mere', 'Mère'),
        ('autre', 'Autre responsable légal ou référent'),
    )
    RESP2 = (
        ('pere','Père'),
        ('mere', 'Mère'),
        ('autre', 'Autre responsable légal ou référent'),
        ('aucun', 'Aucun')
    )
    resp1 = models.CharField(max_length=5, choices=RESP1,
                             default='mere', verbose_name="Lien de parenté")
    nom_resp1 = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom_resp1 = models.CharField(max_length=255, verbose_name="Prénom")
    adresse_resp1 = AddressField(verbose_name="Adresse", related_name='resp1')
    email_resp1 = models.EmailField(max_length=255, verbose_name="Email")
    tel_resp1 = PhoneNumberField(verbose_name="Numéro de téléphone")
    sociopro_resp1 = models.ForeignKey(Sociopro, related_name='resp1',
                                       on_delete=models.CASCADE, verbose_name="Profession")
    resp2 = models.CharField(max_length=5, choices=RESP2,
                                default='pere', verbose_name="Lien de parenté")
    nom_resp2 = models.CharField(max_length=255, verbose_name="Nom de famille", blank=True, null=True)
    prenom_resp2 = models.CharField(max_length=255, verbose_name="Prénom", blank=True, null=True)
    adresse_resp2 = AddressField(verbose_name="Adresse", related_name='resp2', blank=True, null=True)
    email_resp2 = models.EmailField(max_length=255, verbose_name="Email", blank=True, null=True)
    tel_resp2 = PhoneNumberField(verbose_name="Numéro de téléphone", blank=True, null=True)
    sociopro_resp2 = models.ForeignKey(Sociopro, related_name='resp2',
                                       on_delete=models.CASCADE, verbose_name="Profession", blank=True, null=True)

    spe1 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '1'}, blank=True, related_name='spe1')
    spe2 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '2'}, blank=True, related_name='spe2')
    spe3 = models.ManyToManyField(Spe, limit_choices_to={'groupe': '3'}, blank=True, related_name='spe3')
    NIVEAU = (
        ('premiere', 'Première'),
        ('deter', 'Détermination (2nde)'),
        ('premiere', 'Première'),
        ('term', 'Terminale'),
        ('crepa','CREPA'),
    )
    niveau = models.CharField(max_length=10, choices=NIVEAU, verbose_name="Niveau d'inscription", default='deter')
    # Scolarité passée
    dys = models.ManyToManyField(TroubleCognitif, verbose_name="Troubles de l'apprentissage")
    allergie = models.ManyToManyField(Allergie, verbose_name="Allergies")

    nouvelle = models.BooleanField(verbose_name='Première inscription au LXP', default=True)
    niveau_an_passe = models.CharField(max_length=10, choices=NIVEAU,
                                       verbose_name="Niveau d'inscription l'an passé", blank=True, null=True)
    gb_an_passe = models.IntegerField(choices=GB,
                                       verbose_name="Groupe de base", blank=True, null=True)
    ecco_an_passe = models.ForeignKey(MEE, on_delete=models.CASCADE,
                                      verbose_name="MEE d'ECCO", blank=True, null=True)

    gb_annee_en_cours = models.IntegerField(choices=GB,
                                      verbose_name="Groupe de base", blank=True, null=True)