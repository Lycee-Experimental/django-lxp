# django-lxp
Un site élaboré avec Django pour gérer les inscriptions au Lycée Expérimental.

A tester ici : https://inscription.cf
## TODO
### Travail sur le formulaire d'inscription
- Renseigner l'ensemble des **champs nécessaires** dans `models.py`
- Mise en forme des étapes du **formulaire** : `forms.py` avec les Layout de Crispy
### Travail sur le graphisme
- Travailler le html+css des différents `templates` pour l'affichage des différentes pages web et PDF.
- Générer d'autres vues `views.py` qui nous sont utiles (fiches d'inscription,liste par Spé, niveau, GB, anciens-nouveau...) : _views.py et templates_
et ainsi les PDF correspondants.
- Modifier l'interface `admin` pour avoir accès à différents menus (liste d'élèves, génération de divers PDF, 
statistiques...)
### Travail sur l'utilisation et les exports de la base de donnée
- Exporter la base sous forme de **CSV** et **xml** pour que cela convienne à Cyclade + Siecle : https://docs.djangoproject.com/fr/4.0/topics/serialization/
- Utilisation des données pour créer des graphiques (évolution du nombre d'inscriptions, diagrammes par genre, par niveau, géolocalisation...), dans l'interface admin.
------

## Informations techniques

### Hébergement et CI/CD

Le **code** est hébergé sur **Github**, et l'intégration et le déploiement continu (**CI/CD**) est assuré par les **[Github Actions](https://github.com/features/actions)**.

L'**application** est automatiquement déployée sur **[Heroku](https://www.heroku.com/)** et les **fichiers statiques** sont hébergés sur **[AWS S3](https://aws.amazon.com/fr/s3/)**, par la librarie storages (backends s3boto3)

Le **nom de domaine** inscription.cf a été reservé chez **[Freenom](https://www.freenom.com/fr/index.html)** et transite par le **CDN** (content delivery network) **[Cloudflare](https://www.cloudflare.com/fr-fr/)** qui fournit le **SSL** (https) ainsi qu'une protection du site contre d'éventuelles attaques.

Les js et css sont hébergés par [jsdelivr](https://www.jsdelivr.com/) :

  - [Jquery 3.6](https://jquery.com) (à déclarer dans le template avant le js de bootstrap)
  - [Bootstrap 5](https://getbootstrap.com/)
  - Les icones de [Fontawesome](https://fontawesome.com)
  - Le thème dark de bootstrap de [Vino Rodrigues](https://vinorodrigues.github.io/bootstrap-dark-5/)

L'ensemble de ces services sont gratuits pour une utilisation basique.

### Django

L'application est contruite avec la version 4 du framework web [django](https://www.djangoproject.com/).

Le formulaire est mis en forme avec la librairie [Crispy-form](https://django-crispy-forms.readthedocs.io/en/latest/)

La génération d'un formulaire en plusieurs étapes (wizard) est obtenue grâce à la librairie [Formtools](https://django-formtools.readthedocs.io/en/latest/).

Le champ Adresse avec assistance de Google Map (c'est mââââl mais bien pratique!) est apporté par la librairie [django-address](https://pypi.org/project/django-address/).

La visualisation de tableaux est simplifiée par la librairie [django-tables2](https://django-tables2.readthedocs.io/en/latest/).

L'export de pages web sous forme de PDF est réalisé par la librairie [Weasyprint](https://weasyprint.org/).

La cartographie est obtenue avec [django-leaflet](https://github.com/makinacorpus/django-leaflet).
