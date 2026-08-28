from django.urls import path
from . import views


urlpatterns = [

    path(
        "passenger/<int:flight_id>/",
        views.passenger_details,
        name="passenger_details"
    ),

    path(
        "seat-selection/<int:booking_id>/",
        views.seat_selection,
        name="seat_selection"
    ),

    path(
        "summary/<int:booking_id>/",
        views.booking_summary,
        name="booking_summary"
    ),

    path(
    "payment/<int:booking_id>/",
    views.payment,
    name="payment"
    ),

    path(
        "payment-success/<int:booking_id>/",
        views.payment_success,
        name="payment_success"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),

    path(
        "ticket/<int:booking_id>/",
        views.ticket,
        name="ticket"
    ),

]
