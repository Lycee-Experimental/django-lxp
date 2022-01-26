# django-lxp
Un site élaboré avec Django pour gérer les inscriptions au Lycée Expérimental.

A tester ici : https://inscription.cf
## TODO
- **Formulaire d'inscription [[#1]](https://github.com/Lycee-Experimental/django-lxp/issues/1)** :
Aboutir à un formulaire permettant le renseignement de toutes les données nécessaires à l'inscription.

- **Fiche d'inscription [[#9]](https://github.com/Lycee-Experimental/django-lxp/issues/9)** :
Générer un PDF de fiche d'inscription qu'il ne restera plus qu'à imprimer et faire signer par élève et familles.

- **Recherche dans les inscriptions** : 
Travailler à une interface permettant de faire des recherches dans la base.

- **Génération d'autres fichiers utiles au secret** : 
Générer différentes vues (`views.py`) qui nous seront utiles (liste d'élèves par Spé, par niveau, par GB, GECCO...) et ainsi les PDF correspondants.
Traitement des données pour créer des graphiques (évolution du nombre d'inscriptions, diagrammes par genre, par niveau, géolocalisation...), dans l'interface admin.

- **Menu d'administration** : 
Modifier l'interface `admin` pour y intégrer différents menus pour accéder aux différentes fonctionalités : modification de fiches, validation des inscriptions, assignation à un groupe de base/ecco, désinscriptions, recherche élèves, génération de divers PDF, 
statistiques, cartographie...)

- **Exports de la base** :
Exporter la base élève dans les formats convenant à un import dans les bases Siecle et Cyclade du rectorat.

## Informations techniques

### Hébergement et CI/CD

Le **code** est hébergé sur **Github**, et l'intégration et le déploiement continu (**CI/CD**) est assuré par les **[Github Actions](https://github.com/features/actions)**.

L'**application** est automatiquement déployée sur **[Heroku](https://www.heroku.com/)**, les **fichiers statiques** sont hébergés sur **[AWS S3](https://aws.amazon.com/fr/s3/)**, par la librarie storages (backends s3boto3), la **base de donnée Posgresql** sur **[AWS RDS]**(https://aws.amazon.com/fr/rds).

Le **nom de domaine** `inscription.cf` a été reservé chez **[Freenom](https://www.freenom.com/fr/index.html)** et transite par le **CDN** (content delivery network) **[Cloudflare](https://www.cloudflare.com/fr-fr/)** qui fournit le **SSL** (https) ainsi qu'une protection du site contre d'éventuelles attaques.

Les js et css sont hébergés par [jsdelivr](https://www.jsdelivr.com/) :

  - [Jquery 3.6](https://jquery.com) (à déclarer dans le template avant le js de bootstrap)
  - [Bootstrap 4](https://getbootstrap.com/)
  - Les icones de [Fontawesome](https://fontawesome.com)

L'ensemble de ces services sont gratuits pour une utilisation basique.

### Django

L'application est contruite avec la version 4 du framework web [django](https://www.djangoproject.com/).

Le formulaire est mis en forme avec la librairie [Crispy-form](https://django-crispy-forms.readthedocs.io/en/latest/)

La génération d'un formulaire en plusieurs étapes (wizard) est obtenue grâce à la librairie [Formtools](https://django-formtools.readthedocs.io/en/latest/).

Le champ Adresse avec assistance de Google Map (c'est mââââl mais bien pratique!) est apporté par la librairie [django-address](https://pypi.org/project/django-address/).

La visualisation de tableaux est simplifiée par la librairie [django-tables2](https://django-tables2.readthedocs.io/en/latest/).

L'export de pages web sous forme de PDF est réalisé par la librairie [Weasyprint](https://weasyprint.org/).

La cartographie est obtenue avec [django-leaflet](https://github.com/makinacorpus/django-leaflet).

L'autompletion de certains champs (commune naissance, département...) est obtenue avec [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light).

La vérification du format des numéros de téléphone se fait avec [django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field)

La possibilité d'avoir une sélection multiple de checkboxes est obtenue avec la librairie [django-multiselectfield](https://github.com/goinnn/django-multiselectfield).

### Boostrap
Bootstrap est un framwork css / js développé initialement pour twitter qui permet l'afficahge de site web responsive. 
On utilise ici un thème dark de bootstrap mis au point par [Vino Rodrigues](https://github.com/vinorodrigues/bootstrap-dark/)

