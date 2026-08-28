"""
URL configuration for flight_booking project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("accounts.urls")),

    # Open website → Login page
    path("", home, name="home"),

    path("flights/", include("flights.urls")),
    path("bookings/", include("bookings.urls")),
]