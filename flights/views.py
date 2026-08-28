from django.shortcuts import render
from .models import Flight
from django.contrib.auth.decorators import login_required


@login_required
def search_flights(request):

    # If user just opens the Search Flights page
    if not request.GET:
        return render(
            request,
            "search_flights.html"
        )

    # Get search values
    source = request.GET.get("from")
    destination = request.GET.get("to")
    departure = request.GET.get("departure")
    travel_class = request.GET.get("class")

    flights = []

    # Search flights only when required fields are available
    if source and destination and departure:

        flights = Flight.objects.filter(
            source__city__iexact=source,
            destination__city__iexact=destination,
            departure_time__date=departure,
            travel_class=travel_class
        )

    return render(
        request,
        "flight_results.html",
        {
            "flights": flights,
            "search_source": source,
            "search_destination": destination,
            "search_date": departure,
            "search_class": travel_class,
        }
    )