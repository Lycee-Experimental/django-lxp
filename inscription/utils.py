import hashlib
import os
import time
from uuid import uuid4
from django.utils import timezone
from django.core.exceptions import ValidationError
# Une librairie pour gérer les tableaux
from django_tables2 import SingleTableView
# Des outils pour redéfinir le Captcha pour qu'il marche dans le wizard
from captcha.fields import CaptchaField
from captcha.conf import settings
from captcha.models import CaptchaStore
from storages.backends.s3boto3 import S3Boto3Storage


class PagedFilteredTableView(SingleTableView):
    """Actualise le tableau en fonction des filtres"""
    filter_class = None
    formhelper_class = None
    context_filter_name = "filter"

    def get_table_data(self):
        self.filter = self.filter_class(
            self.request.GET, queryset=super().get_table_data()
        )
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data(**kwargs)
        context[self.context_filter_name] = self.filter
        return context


class CaptchaWizardField(CaptchaField):
    """Une classe pour redéfinir le captcha pour qu'il marche avec le wizard (double vérif)
    """

    def __init__(self, *args, **kwargs):
        self.validity_count = kwargs.pop('validity_count', 2)
        self.validity_cache = {}
        super(CaptchaWizardField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CaptchaField, self).clean(value)
        CaptchaStore.remove_expired()
        response, value[1] = (value[1] or '').strip().lower(), ''
        hashkey = value[0]
        if settings.CAPTCHA_TEST_MODE and response.lower() == 'passed':
            # automatically pass the test
            try:
                # try to delete the captcha based on its hash
                CaptchaStore.objects.get(hashkey=hashkey).delete()
            except CaptchaStore.DoesNotExist:
                # ignore errors
                pass
        elif not self.required and not response:
            pass
        else:
            # let enable validity_count times
            # of clean() method
            if hashkey in self.validity_cache and self.validity_cache[hashkey] > 0:
                self.validity_cache[hashkey] -= 1
                return value
            try:
                captcha = CaptchaStore.objects.get(response=response, hashkey=hashkey, expiration__gt=timezone.now())
                self.validity_cache[hashkey] = self.validity_count - 1
                captcha.delete()
            except CaptchaStore.DoesNotExist:
                raise ValidationError(getattr(self, 'error_messages', {}).get('invalid', 'Invalid CAPTCHA'))
        return value


def nom_photo(instance, filename):
    """"Définit le nom de la photo uploadée à partir du nom/prénom de l'élève."""
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.nom and instance.prenom:
        filename = '{}_{}.{}'.format(instance.nom, instance.prenom, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def coordonnees(base):
    """Renvoie une liste contenant les coordonnées [latitude, longitude] de chaque élève.
    Pour affichage avec leaflet."""
    adresses=[]
    for eleve in base:
        adresses.append([eleve.address.latitude, eleve.address.longitude])
    return adresses


def create_hash():
    """Génère une chaine de 10 caractères aléatoires"""
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return  hash.hexdigest()[:-10]


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
