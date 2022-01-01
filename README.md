# django-lxp
Un site élaboré avec Django pour gérer les inscriptions au Lycée Expérimental.

A tester ici : https://inscription.cf
## TODO
### Travail sur le formulaire d'inscription
- Renseigner l'ensemble des **champs nécessaires** dans `models.py`
- Mise en forme des étapes du **formulaire** : `forms.py` avec les Layout de Crispy
### Travail sur le graphisme
- Travailler le html+css des différents `templates` pour l'affichage des différentes pages web et PDF.
- Générer d'autres vues `views.py` qui nous sont utiles (fiches d'inscription,liste par Spé, niveau, GB, anciens-nouveau...) : _views.py et templates_.
et les PDF correspondants.
- Modifier l'interface `admin` pour avoir accès à différents menus (liste d'élèves, génération de divers PDF, 
statistiques...)
### Travail sur l'utulisation et les exports de la base de donnée
- Exporter la base sous forme de **CSV** et **xml** pour que cela convienne à Cyclade + Siecle : https://docs.djangoproject.com/fr/4.0/topics/serialization/
- Utilisation des données pour créer des graphiques (évolution du nombre d'inscriptions, diagrammes par genre, par niveau, géolocalisation...), dans l'interface admin.
------

## Informations techniques

Le site est déployé sur Heroku, les statics hébergés sur AWS S3, le https fourni par Cloudflare et le nom de domaine chez freenom... Tout est gratuit !

Le formulaire est créé avec la librairie crispy-form : https://django-crispy-forms.readthedocs.io/en/latest/
et le wizard de formtool pour qu'il se remplisse en plusieurs étapes.

Les js et css sont hébergées par jsdelivr :

    - Jquery 3.6 (à déclarer avant le js de bootstrap) : https://jquery.com/download/
    - Botstrap 5 : https://getbootstrap.com/docs/5.0/getting-started/download/
    - Les icones de Fontawesome : https://fontawesome.com/download
    - Le thème dark utilisé est celui-ci : https://vinorodrigues.github.io/bootstrap-dark-5/

