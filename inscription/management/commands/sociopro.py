import csv
from django.core.management import BaseCommand
from django.utils import timezone

from inscription.models import Sociopro


class Command(BaseCommand):
    help = "Charge la liste des catégories sociopro depuis un fichier CSV."

    def handle(self, *args, **options):
        start_time = timezone.now()
        with open('inscription/data/sociopro.csv', "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            for row in data:
                Sociopro.objects.create(code=row[0], name=row[1])
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Le chargement a pris: {(end_time-start_time).total_seconds()} seconds."
            )
        )
