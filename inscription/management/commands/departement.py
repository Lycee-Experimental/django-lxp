import csv
from django.core.management import BaseCommand
from django.utils import timezone

from inscription.models import Departement


class Command(BaseCommand):
    help = "Loads products and product categories from CSV file."

    def handle(self, *args, **options):
        start_time = timezone.now()
        with open('inscription/data/departement.csv', "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            for row in data:
                Departement.objects.create(code=row[0], nom=row[1])
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
