from django.contrib import admin
from .models import Booking, Passenger

class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['pnr', 'train', 'travel_class', 'journey_date', 'total_fare', 'status', 'booking_date']
    search_fields = ['pnr']
    inlines = [PassengerInline]  # ← Booking page la passengers also show aagum

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'seat_number', 'coach', 'booking']
    search_fields = ['name', 'booking__pnr']