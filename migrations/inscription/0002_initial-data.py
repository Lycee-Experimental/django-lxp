from django.core.management import call_command
from django.db import migrations

def forwards_func(apps, schema_editor):
    fixtures = ['mee', 'sociopro', 'spe', 'pays', 'departement',  'commune', 'etablissement']
    for fixture in fixtures:
        try:
            call_command('loaddata', fixture, verbosity=2)
        except:
            print("Erreur de l'import des données initiales. Commencer par les télécharger.")

def reverse_func(apps, schema_editor):
    print('reverse')

class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]

