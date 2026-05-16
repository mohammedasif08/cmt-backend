from django.db import models

class Train(models.Model):
    train_number = models.CharField(max_length=10)
    train_name = models.CharField(max_length=100)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    from_code = models.CharField(max_length=10, default='')
    to_code = models.CharField(max_length=10, default='')
    departure_time = models.CharField(max_length=10)
    arrival_time = models.CharField(max_length=10)
    duration = models.CharField(max_length=20)
    train_type = models.CharField(max_length=50)
    classes = models.JSONField(default=list)
    fare = models.JSONField(default=dict)
    total_seats = models.JSONField(default=dict)
    booked_seats = models.JSONField(default=dict)
    seat_gender = models.JSONField(default=dict)
    days = models.JSONField(default=list)
    rating = models.FloatField(default=4.0)
    amenities = models.JSONField(default=list)

    def __str__(self):
        return f"{self.train_number} - {self.train_name}"

class Booking(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=10)
    coach = models.CharField(max_length=10)
    booking_date = models.DateTimeField(auto_now_add=True)
    pnr = models.CharField(max_length=20, unique=True)