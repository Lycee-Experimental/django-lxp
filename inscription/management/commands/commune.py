import csv
from django.core.management import BaseCommand
from django.utils import timezone

from inscription.models import Departement, Commune


class Command(BaseCommand):
    help = "Importation des commune depuis le fichier commune.csv."

    def handle(self, *args, **options):
        start_time = timezone.now()
        with open('inscription/data/commune.csv', "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            for row in data:
                if row[0][:2] == '97':
                    dep_code = row[0][:3]
                else:
                    dep_code = '0'+row[0][:2]
                departement = Departement.objects.get(code=dep_code)
                Commune.objects.create(
                    code=row[0],
                    nom=row[1],
                    departement=departement
                )
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )