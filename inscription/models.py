from django.db import models
from django_countries.fields import CountryField
from address.models import AddressField
from .utils import nom_photo, create_hash


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

    STREET_TYPE_CHOICES = (
        ('Boulevard', 'Boulevard'),
        ('Avenue', 'Avenue'),
        ('Cours', 'Cours'),
        ('Place', 'Place'),
        ('Rue', 'Rue'),
        ('Route', 'Route'),
        ('Voie', 'Voie'),
        ('Chemin', 'Chemin'),
        ('Square', 'Square'),
        ('Impasse', 'Impasse'),
        ('Rond-point', 'Rond-point'),
        ('Quai', 'Quai')
    )

    commune_naissance = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune de naissance")
    departement_naissance = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département de naissance")
    address = AddressField(verbose_name="Adresse")
    civility = models.CharField(max_length=3, choices=CIVILITY_CHOICES,
                                default='M.', verbose_name="Civilité")
    last_name = models.CharField(max_length=255, verbose_name="Nom de famille")
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    birth_date = models.DateField(verbose_name="Date de naissance")
    birth_place = models.CharField(max_length=255, verbose_name="Ville de naissance")
    birth_country = CountryField(max_length=255, verbose_name="Pays de naissance")
    mail = models.EmailField(max_length=255, verbose_name="Mail")
    street_type = models.CharField(max_length=30, verbose_name="Type de rue",
                                   choices=STREET_TYPE_CHOICES, default='Rue')
    street_number = models.CharField(max_length=30, verbose_name="Numéro de rue")
    street = models.CharField(max_length=30, verbose_name="Rue")
    comp_1 = models.CharField(max_length=255, verbose_name="Complément 1",
                              blank=True, null=True)
    comp_2 = models.CharField(max_length=255, verbose_name="Complément 2",
                              blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="Ville")
    zip_code = models.CharField(max_length=255, verbose_name="Code postal")
    country = CountryField(max_length=255, verbose_name="Pays")
    phone = models.CharField(max_length=255, blank=True, null=True,
                             verbose_name="Téléphone")
    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    hash = models.CharField(max_length=30, default=create_hash, unique=True)
    photo = models.ImageField(upload_to=nom_photo, null=True)


