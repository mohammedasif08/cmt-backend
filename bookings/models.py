from django.db import models
from trains.models import Train

class Booking(models.Model):
    pnr = models.CharField(max_length=20, unique=True)
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='bookings'   # ← ithu add panninom — conflict fix
    )
    journey_date = models.DateField()
    travel_class = models.CharField(max_length=5)
    total_fare = models.IntegerField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"PNR: {self.pnr}"

class Passenger(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='passengers'
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    coach = models.CharField(max_length=10, default='S1')

    def __str__(self):
        return f"{self.name} - {self.booking.pnr}"