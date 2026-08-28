from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from flights.models import Flight
from .models import Booking, Passenger


@login_required
def passenger_details(request, flight_id):

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            total_amount=flight.price,
            status="Confirmed"
        )

        Passenger.objects.create(
            booking=booking,
            full_name=full_name,
            age=age,
            gender=gender,
            email=email,
            phone=phone
        )

        return redirect(
            "seat_selection",
            booking_id=booking.id
        )

    return render(
        request,
        "passenger_details.html",
        {
            "flight": flight
        }
    )


@login_required
def seat_selection(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    passenger = booking.passengers.first()

    booked_seats = set(
        Passenger.objects.filter(
            booking__flight=booking.flight
        ).exclude(
            booking=booking
        ).values_list(
            "seat_number",
            flat=True
        )
    )

    # Create aircraft seat map
    seat_rows = []

    for row in range(1, 19):

        seat_rows.append({
            "number": row,
            "A": f"{row}A",
            "B": f"{row}B",
            "C": f"{row}C",
            "D": f"{row}D",
        })


    if request.method == "POST":

        seat_number = request.POST.get("seat_number")

        if not seat_number:

            messages.error(
                request,
                "Please select a seat."
            )

            return redirect(
                "seat_selection",
                booking_id=booking.id
            )


        # Check if seat is already booked
        if seat_number in booked_seats:

            messages.error(
                request,
                f"Seat {seat_number} is already booked."
            )

            return redirect(
                "seat_selection",
                booking_id=booking.id
            )


        with transaction.atomic():

            flight = Flight.objects.select_for_update().get(
                id=booking.flight.id
            )

            if flight.available_seats <= 0:

                messages.error(
                    request,
                    "No seats are available on this flight."
                )

                return redirect(
                    "seat_selection",
                    booking_id=booking.id
                )


            passenger.seat_number = seat_number
            passenger.save()


            flight.available_seats -= 1
            flight.save()


        return redirect(
            "booking_summary",
            booking_id=booking.id
        )


    return render(
        request,
        "seat_selection.html",
        {
            "booking": booking,
            "passenger": passenger,
            "seat_rows": seat_rows,
            "booked_seats": booked_seats,
        }
    )

@login_required
def booking_summary(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    passenger = booking.passengers.first()

    return render(
        request,
        "booking_summary.html",
        {
            "booking": booking,
            "passenger": passenger
        }
    )


@login_required
def payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    passenger = booking.passengers.first()

    booked_seats = set(
        Passenger.objects.filter(
            booking__flight=booking.flight,
            booking__status="Confirmed"
        ).exclude(
            booking=booking
        ).values_list(
            "seat_number",
            flat=True
        )
    )
    if request.method == "POST":

        payment_method = request.POST.get(
            "payment_method"
        )

        if not payment_method:

            messages.error(
                request,
                "Please select a payment method."
            )

            return redirect(
                "payment",
                booking_id=booking.id
            )

        return redirect(
            "payment_success",
            booking_id=booking.id
        )

    return render(
        request,
        "payment.html",
        {
            "booking": booking,
            "passenger": passenger
        }
    )


@login_required
def payment_success(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    booking.status = "Confirmed"
    booking.save()

    passenger = booking.passengers.first()

    return render(
        request,
        "ticket.html",
        {
            "booking": booking,
            "passenger": passenger,
        }
    )

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).prefetch_related(
        "passengers"
    ).select_related(
        "flight",
        "flight__airline",
        "flight__source",
        "flight__destination"
    ).order_by("-booking_date")

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings
        }
    )
@login_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == "POST":

        # Only cancel confirmed bookings
        if booking.status == "Confirmed":

            passenger = booking.passengers.first()

            with transaction.atomic():

                flight = Flight.objects.select_for_update().get(
                    id=booking.flight.id
                )

                # Return the seat to available inventory
                if passenger and passenger.seat_number:

                    flight.available_seats += 1
                    flight.save()

                    passenger.seat_number = ""
                    passenger.save()

                booking.status = "Cancelled"
                booking.save()

            messages.success(
                request,
                f"Booking #{booking.id} has been cancelled successfully."
            )

        else:

            messages.info(
                request,
                "This booking has already been cancelled."
            )

    return redirect("my_bookings")

@login_required
def ticket(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    passenger = booking.passengers.first()

    return render(
        request,
        "ticket.html",
        {
            "booking": booking,
            "passenger": passenger,
        }
    )


