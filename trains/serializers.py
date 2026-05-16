from rest_framework import serializers
from .models import Train, Booking

class TrainSerializer(serializers.ModelSerializer):
    # Frontend expects camelCase — so we map here
    fromStation = serializers.CharField(source='from_station')
    toStation = serializers.CharField(source='to_station')
    fromCode = serializers.CharField(source='from_code')
    toCode = serializers.CharField(source='to_code')
    departureTime = serializers.CharField(source='departure_time')
    arrivalTime = serializers.CharField(source='arrival_time')
    trainNumber = serializers.CharField(source='train_number')
    trainName = serializers.CharField(source='train_name')
    trainType = serializers.CharField(source='train_type')
    totalSeats = serializers.JSONField(source='total_seats')
    bookedSeats = serializers.JSONField(source='booked_seats')

    class Meta:
        model = Train
        fields = [
            'id',
            'trainNumber',
            'trainName',
            'fromStation',
            'toStation',
            'fromCode',
            'toCode',
            'departureTime',
            'arrivalTime',
            'duration',
            'trainType',
            'classes',
            'fare',
            'totalSeats',
            'bookedSeats',
            'days',
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'