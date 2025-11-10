from django.core.management.base import BaseCommand
from django.utils import timezone
from rentals.models import RentalLog, Cubicle

class Command(BaseCommand):
    help = 'Releases cubicles whose rental time has expired.'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_rentals = RentalLog.objects.filter(
            scheduled_end_time__lte=now,
            is_active=True
        )

        for rental_log in expired_rentals:
            cubicle = rental_log.cubicle
            cubicle.status = 'disponible'
            cubicle.save()

            rental_log.is_active = False
            rental_log.actual_end_time = now
            rental_log.save()

            self.stdout.write(self.style.SUCCESS(f'Cubicle {cubicle.name} (Rental ID: {rental_log.id}) released due to expiration.'))
        
        if not expired_rentals.exists():
            self.stdout.write(self.style.SUCCESS('No expired cubicles to release.'))
