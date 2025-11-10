import csv
from django.core.management.base import BaseCommand
from rentals.models import Student, Career

class Command(BaseCommand):
    help = 'Import students from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                control_number = row['numero_control']
                full_name = row['nombre_completo']
                career_name = row['carrera']

                career, _ = Career.objects.get_or_create(name=career_name)

                student, created = Student.objects.update_or_create(
                    control_number=control_number,
                    defaults={
                        'full_name': full_name,
                        'career': career
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created student {full_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Successfully updated student {full_name}'))
