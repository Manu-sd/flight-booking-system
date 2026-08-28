from django.contrib import admin
from .models import Airline, Airport, Flight


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "code")
    search_fields = ("name", "city", "country", "code")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "airline",
        "source",
        "destination",
        "departure_time",
        "arrival_time",
        "price",
        "travel_class",
        "available_seats",
    )

    list_filter = (
        "airline",
        "travel_class",
        "source",
        "destination",
    )

    search_fields = (
        "flight_number",
        "airline__name",
        "source__city",
        "destination__city",
    )