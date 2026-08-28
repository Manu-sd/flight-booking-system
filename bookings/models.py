from django.db import models
from django.contrib.auth.models import User
from flights.models import Flight


class Booking(models.Model):
    STATUS_CHOICES = [
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Confirmed"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"


class Passenger(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="passengers"
    )

    full_name = models.CharField(
        max_length=150
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    seat_number = models.CharField(
        max_length=10,
        blank=True
    )

    def __str__(self):
        return self.full_name