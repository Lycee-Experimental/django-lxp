import hashlib
import signal
import os
import time
from abc import ABC
from uuid import uuid4
from django.utils import timezone
from django.core.exceptions import ValidationError
# Une librairie pour gérer les tableaux
from django_tables2 import SingleTableView
# Des outils pour redéfinir le Captcha pour qu'il marche dans le wizard
from captcha.fields import CaptchaField
# from captcha.conf import settings
from captcha.models import CaptchaStore
from datetime import datetime, timedelta
from urllib.parse import urlencode
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage
from django.http import HttpResponse
import csv
from storages.utils import clean_name
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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
        # On récupère le "titre" dans l'url pour l'afficher dans le template (context) 
        context["titre"] = self.request.GET.get('titre')
        return context


def generate_pdf(html):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--headless')
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("data:text/html;charset=utf-8,"+html)

    # use can defined additional parameters if needed : https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-printToPDF
    params = {'landscape': False,
              'paperWidth': 8.27,
              'paperHeight': 11.69,
              'printBackground': True,
              'scale': 0.45
              }
              # displayHeaderFooter
              # headerTemplate ( date,title, url, pageNumber, totalPages)
              # footerTemplate
    data = driver.execute_cdp_cmd("Page.printToPDF", params)
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()
    return base64.b64decode(data['data'])


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
        if response.lower() == 'passed':
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
    if instance.nom_famille and instance.prenoms:
        filename = '{}_{}.{}'.format(instance.nom_famille, instance.prenoms, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def coordonnees(base):
    """Renvoie une liste contenant les coordonnées [latitude, longitude] de chaque élève.
    Pour affichage avec leaflet."""
    adresses = []
    for eleve in base:
        if eleve.address:
            adresses.append([eleve.address.latitude, eleve.address.longitude])
    return adresses


def create_hash():
    """Génère une chaine de 10 caractères aléatoires"""
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return hash.hexdigest()[:-10]


## Export de la base en csc
def download_csv(request, queryset):
    # if not request.user.is_staff:
    #  raise PermissionDenied

    model = queryset.model
    model_fields = model._meta.fields
    field_names = [field.name for field in model_fields]
    model_fields_many = model._meta.many_to_many
    field_names_many = [field.name for field in model_fields_many]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    # the csv writer
    writer = csv.writer(response, delimiter=";")
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        for field in field_names_many:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = list(getattr(row, field).all().values_list('intitule', flat=True)) or ''
                    print(value)

                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        writer.writerow(values)
    return response


class OracleStorage(S3Boto3Storage, ABC):
    """Gestion du stockage sur Oracle"""
    def url(self, name, parameters=None, expire=None, http_method=None):
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = self.querystring_expire

        if not self.custom_domain:
            raise Exception('Must set AWS_S3_CUSTOM_DOMAIN')

        if not settings.ORACLE_BUCKET_NAME:
            raise Exception('Must set ORACLE_BUCKET_NAME')

        url = '{}//{}/{}/{}{}'.format(
            self.url_protocol,
            self.custom_domain,
            settings.ORACLE_BUCKET_NAME,
            filepath_to_uri(name),
            '?{}'.format(urlencode(params)) if params else '',
        )

        if self.querystring_auth and self.cloudfront_signer:
            expiration = datetime.utcnow() + timedelta(seconds=expire)
            return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

        return url


class StaticStorage(OracleStorage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(OracleStorage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
