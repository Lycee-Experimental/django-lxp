# Generated by Django 4.1.4 on 2022-12-22 15:06

import address.models
from django.db import migrations, models
import django.db.models.deletion
import inscription.utils
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergene', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, unique=True, verbose_name='Code INSEE')),
                ('name', models.CharField(max_length=50, verbose_name='Département')),
            ],
        ),
        migrations.CreateModel(
            name='Etablissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_commune', models.CharField(max_length=50, null=True)),
                ('code_commune', models.CharField(max_length=6, null=True)),
                ('appartenance_education_prioritaire', models.CharField(blank=True, max_length=50, null=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('code_nature', models.IntegerField(null=True)),
                ('nombre_d_eleves', models.CharField(blank=True, max_length=50, null=True)),
                ('type_etablissement', models.CharField(max_length=50, null=True)),
                ('libelle_nature', models.CharField(max_length=50, null=True)),
                ('nom_etablissement', models.CharField(max_length=150, null=True)),
                ('identifiant_de_l_etablissement', models.CharField(max_length=10, null=True)),
                ('statut_public_prive', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langue', models.CharField(max_length=10, unique=True, verbose_name='Langue')),
                ('siecle', models.CharField(max_length=2, verbose_name='Code Siecle')),
                ('cyclades', models.CharField(max_length=10, verbose_name='Code Cyclades')),
            ],
        ),
        migrations.CreateModel(
            name='MEE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=20, unique=True, verbose_name='Prénom')),
                ('gb_an_passe', models.IntegerField(blank=True, choices=[(1, 'G1'), (2, 'G2'), (3, 'G3'), (4, 'G4'), (5, 'G5')], null=True, verbose_name="GB de l'an passé")),
                ('gb_annee_en_cours', models.IntegerField(blank=True, choices=[(1, 'G1'), (2, 'G2'), (3, 'G3'), (4, 'G4'), (5, 'G5')], null=True, verbose_name='GB de cette année')),
            ],
        ),
        migrations.CreateModel(
            name='Sociopro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, unique=True, verbose_name='Code Sociopro')),
                ('name', models.CharField(max_length=100, verbose_name='Catégorie sociopro')),
            ],
        ),
        migrations.CreateModel(
            name='Spe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code Spé')),
                ('intitule', models.CharField(max_length=50, verbose_name='Intitulé Spé')),
                ('groupe', models.CharField(blank=True, max_length=2, null=True, verbose_name='Groupe Spé')),
                ('type', models.CharField(blank=True, max_length=10, null=True, verbose_name='Type Spé')),
            ],
        ),
        migrations.CreateModel(
            name='TroubleCognitif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trouble', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='Code INSEE')),
                ('name', models.CharField(max_length=50, verbose_name='Département')),
            ],
            options={
                'unique_together': {('code', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, verbose_name='Code INSEE')),
                ('name', models.CharField(max_length=50, verbose_name='Commune')),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.departement', to_field='code', verbose_name='Département')),
            ],
            options={
                'unique_together': {('code', 'name')},
            },
        ),
        migrations.CreateModel(
            name='BaseEleve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_naissance', models.DateField(verbose_name='Date de naissance')),
                ('ville_naissance_etrangere', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ville natale')),
                ('civilite', models.CharField(choices=[('M.', 'M.'), ('MME', 'Mme')], default='MME', help_text="Quel sexe t'est attribué dans les documents administratifs ?", max_length=3, verbose_name='Civilité')),
                ('genre', models.CharField(choices=[('il', 'Il'), ('elle', 'Elle'), ('iel', 'Il, Elle, Iel ou autre')], default='elle', help_text="Veux-tu que l'on parle de toi en disant il, elle, iel ou autre ?", max_length=5, verbose_name='Pronom')),
                ('nom_famille', models.CharField(max_length=255, verbose_name='Nom de famille')),
                ('prenoms', models.CharField(max_length=255, verbose_name='Prénom')),
                ('prenom_usage', models.CharField(blank=True, help_text='Souhaites-tu être appelé autrement que par ton prénom administratif ?', max_length=255, null=True, verbose_name="Prénom d'usage")),
                ('adresse_mail', models.EmailField(help_text="Prends le temps de te créer une adresse email si tu n'en as pas encore.", max_length=255, verbose_name='Email')),
                ('telephone_mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Téléphone')),
                ('projet', models.TextField(help_text='Détaille ici ton projet : pourquoi faire le choix du Lycée Expérimental ?', verbose_name='Projet au LXP')),
                ('hash', models.CharField(default=inscription.utils.create_hash, max_length=30, unique=True)),
                ('photo', models.ImageField(blank=True, help_text="Merci de téléverser une photo pour ta fiche d'inscription.", null=True, upload_to=inscription.utils.nom_photo)),
                ('resp1', models.CharField(choices=[('pere', 'Père'), ('mere', 'Mère'), ('autre', 'Autre responsable légal ou référent')], default='mere', max_length=5, verbose_name='Lien de parenté ou autre')),
                ('civilite_resp1', models.CharField(choices=[('M.', 'M.'), ('MME', 'Mme')], default='M.', max_length=3, verbose_name='Civilité')),
                ('nom_resp1', models.CharField(max_length=255, verbose_name='Nom de famille')),
                ('prenom_resp1', models.CharField(max_length=255, verbose_name='Prénom')),
                ('email_resp1', models.EmailField(max_length=255, verbose_name='Email')),
                ('tel_resp1', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro de téléphone')),
                ('resp2', models.CharField(choices=[('pere', 'Père'), ('mere', 'Mère'), ('autre', 'Autre responsable légal ou référent·e'), ('aucun', "Pas d'autre référent·e")], default='pere', max_length=5, verbose_name='Lien de parenté')),
                ('civilite_resp2', models.CharField(blank=True, choices=[('M.', 'M.'), ('MME', 'Mme')], default='M.', max_length=3, null=True, verbose_name='Civilité')),
                ('nom_resp2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom de famille')),
                ('prenom_resp2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Prénom')),
                ('email_resp2', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('tel_resp2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Numéro de téléphone')),
                ('niveau', models.CharField(choices=[('deter', 'Détermination (2nde)'), ('premiere', 'Première'), ('term', 'Terminale'), ('crepa', 'CREPA')], default='deter', max_length=10, verbose_name="Niveau d'inscription")),
                ('amenagements', models.BooleanField(default=False, help_text="As-tu déjà bénéficié d'aménagement d'épreuves pour ces troubles ?", verbose_name="Aménagements d'épreuves")),
                ('boursier', models.BooleanField(default=False, help_text="Étais-tu boursier·e l'an passé ?", verbose_name='Bénéficiaire de bourses')),
                ('desco', models.BooleanField(default=False, help_text="Étais-tu déscolarisé·e l'an passé ?", verbose_name='Déscolarisation')),
                ('ancien', models.BooleanField(default=False, help_text="Étais-tu inscrit·e au LXP l'an passé ?", verbose_name='Réinscription au LXP')),
                ('date_entretien', models.DateField(blank=True, help_text="Indique une date approximative si tu n'as plus la date exacte.", null=True, verbose_name='Date de ton entretien')),
                ('niveau_an_passe', models.CharField(blank=True, choices=[('deter', 'Détermination (2nde)'), ('premiere', 'Première'), ('term', 'Terminale'), ('crepa', 'CREPA')], max_length=10, null=True, verbose_name="Niveau d'inscription l'an passé")),
                ('gb_an_passe', models.IntegerField(blank=True, choices=[(1, 'G1'), (2, 'G2'), (3, 'G3'), (4, 'G4'), (5, 'G5')], null=True, verbose_name='Groupe de base')),
                ('gb_annee_en_cours', models.IntegerField(blank=True, choices=[(1, 'G1'), (2, 'G2'), (3, 'G3'), (4, 'G4'), (5, 'G5')], null=True, verbose_name='Groupe de base')),
                ('address', address.models.AddressField(blank=True, help_text="Si tu n'as pas encore d'addresse dans les environs de Saint-Nazaire, laisse ce champ vide.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleve', to='address.address', verbose_name='Adresse')),
                ('adresse_resp1', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, related_name='resp1', to='address.address', verbose_name='Adresse')),
                ('adresse_resp2', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resp2', to='address.address', verbose_name='Adresse')),
                ('allergies', models.ManyToManyField(blank=True, null=True, to='inscription.allergie', verbose_name='Allergies')),
                ('commune_naissance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inscription.commune', verbose_name='Commune de naissance')),
                ('depCOM_naissance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inscription.departement', verbose_name='Département de naissance')),
                ('ecco_an_passe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ecco', to='inscription.mee', verbose_name="MEE d'ECCO")),
                ('etablissement_origine', models.ForeignKey(blank=True, help_text='Où étiez-vous avant de vous inscrire au Lycée Expérimental ?', null=True, on_delete=django.db.models.deletion.CASCADE, to='inscription.etablissement', verbose_name="Etablissement d'origine")),
                ('lv1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lv1', to='inscription.lv', verbose_name='Première langue vivante')),
                ('lv2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lv2', to='inscription.lv', verbose_name='Deuxième langue vivante')),
                ('mee_entretien', models.ForeignKey(blank=True, help_text='Laisse vide si tu ne te souviens plus du prénom du/de la MEE que tu as rencontré.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entretien', to='inscription.mee', verbose_name="MEE d'entretien")),
                ('nationalite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nationalite', to='inscription.pays', verbose_name='Nationalité')),
                ('pays_naissance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.pays', verbose_name='Pays de naissance')),
                ('sociopro_resp1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resp1', to='inscription.sociopro', verbose_name='Profession')),
                ('sociopro_resp2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resp2', to='inscription.sociopro', verbose_name='Profession')),
                ('spe1', models.ManyToManyField(blank=True, limit_choices_to={'groupe': '1'}, null=True, related_name='spe1', to='inscription.spe')),
                ('spe2', models.ManyToManyField(blank=True, limit_choices_to={'groupe': '2'}, null=True, related_name='spe2', to='inscription.spe')),
                ('spe3', models.ManyToManyField(blank=True, limit_choices_to={'groupe': '3'}, null=True, related_name='spe3', to='inscription.spe')),
                ('spes', models.ManyToManyField(blank=True, null=True, related_name='spes', to='inscription.spe')),
                ('troubles', models.ManyToManyField(blank=True, help_text="As-tu des troubles de l'apprentissage ou une situation médicale impactant ta scolarité ?", null=True, to='inscription.troublecognitif', verbose_name="Troubles de l'apprentissage")),
            ],
        ),
    ]
