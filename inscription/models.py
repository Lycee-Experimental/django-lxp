from django.db import models
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField
from .utils import nom_photo, create_hash


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
        ('Il', 'Il'),
        ('Elle', 'Elle'),
        ('Iel', 'Iel')
    )
    date_naissance = models.DateField(verbose_name="Date de naissance")
    commune_naissance = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Commune de naissance")
    departement_naissance = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="Département de naissance")
    pays_naissance = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="Pays de naissance")
    address = AddressField(verbose_name="Adresse", related_name='eleve')
    civility = models.CharField(max_length=3, choices=CIVILITY_CHOICES,
                                default='M.', verbose_name="Civilité")
    genre = models.CharField(max_length=5, choices=GENRE, verbose_name='Pronom', default='Iel',
                             help_text="Veux-tu que l'on parle de toi en disant il, elle ou iel ?")
    nom = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    nom_usage = models.CharField(max_length=255, verbose_name="Nom d'usage")
    email = models.EmailField(max_length=255, verbose_name="Email")
    telephone = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name="Téléphone")
    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    hash = models.CharField(max_length=30, default=create_hash, unique=True)
    photo = models.ImageField(upload_to=nom_photo, null=True)
    # RESPONSABLES
    RESP = (
        ('pere','Père'),
        ('mere', 'Mère'),
        ('autre', 'Autre responsable légal ou référent')
    )
    resp2 = models.BooleanField(verbose_name="Deuxième responsable")
    nom_resp1 = models.CharField(max_length=255, verbose_name="Nom de famille")
    nom_resp2 = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom_resp1 = models.CharField(max_length=255, verbose_name="Prénom")
    prenom_resp2 = models.CharField(max_length=255, verbose_name="Prénom")
    type_resp1 = models.CharField(max_length=5, choices=RESP,
                                default='mere', verbose_name="Lien de parenté")
    type_resp2 = models.CharField(max_length=5, choices=RESP,
                                default='mere', verbose_name="Lien de parenté")
    adresse_resp1 = AddressField(verbose_name="Adresse", related_name='rep1')
    adresse_resp2 = AddressField(verbose_name="Adresse", related_name='rep2')
    email_resp1 = models.EmailField(max_length=255, verbose_name="Email")
    email_resp2 = models.EmailField(max_length=255, verbose_name="Email")
    tel_resp1 = PhoneNumberField(verbose_name="Numéro de téléphone")
    tel_resp2 = PhoneNumberField(verbose_name="Numéro de téléphone")
    sociopro_resp1 = models.ForeignKey(Sociopro, related_name='rep1',
                                       on_delete=models.CASCADE, verbose_name="Profession")
    sociopro_resp2 = models.ForeignKey(Sociopro, related_name='resp2',
                                       on_delete=models.CASCADE, verbose_name="Profession")

