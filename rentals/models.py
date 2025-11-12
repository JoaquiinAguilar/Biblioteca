from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Career(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    control_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} ({self.control_number})'

class Cubicle(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')

    def __str__(self):
        return self.name

class RentalLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cubicle = models.ForeignKey(Cubicle, on_delete=models.CASCADE)
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    requested_duration = models.PositiveIntegerField(help_text="Duración en minutos")
    scheduled_start_time = models.DateTimeField(auto_now_add=True)
    scheduled_end_time = models.DateTimeField()
    actual_end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo registro
            self.scheduled_end_time = timezone.now() + datetime.timedelta(minutes=self.requested_duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reserva de {self.cubicle.name} por {self.student.full_name}'