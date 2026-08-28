from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airport(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    CLASS_CHOICES = [
        ("Economy", "Economy"),
        ("Premium Economy", "Premium Economy"),
        ("Business", "Business"),
        ("First Class", "First Class"),
    ]

    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE
    )

    flight_number = models.CharField(max_length=20, unique=True)

    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departure_flights"
    )

    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrival_flights"
    )

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    travel_class = models.CharField(
        max_length=30,
        choices=CLASS_CHOICES,
        default="Economy"
    )

    total_seats = models.PositiveIntegerField(default=180)

    available_seats = models.PositiveIntegerField(default=180)

    def __str__(self):
        return f"{self.flight_number}: {self.source.code} → {self.destination.code}"