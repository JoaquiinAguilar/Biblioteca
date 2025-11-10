import csv
from django.core.management.base import BaseCommand
from rentals.models import Cubicle

class Command(BaseCommand):
    help = 'Import cubicles from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['nombre']
                capacity = row['capacidad']

                cubicle, created = Cubicle.objects.update_or_create(
                    name=name,
                    defaults={
                        'capacity': capacity,
                        'status': 'disponible'
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created cubicle {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Successfully updated cubicle {name}'))
