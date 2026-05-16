import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Passenger
from .serializers import BookingSerializer

def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))

@api_view(['POST'])
def create_booking(request):
    data = request.data
    pnr = generate_pnr()

    try:
        booking = Booking.objects.create(
            pnr=pnr,
            train_id=data['train_id'],
            journey_date=data['journey_date'],
            travel_class=data['travel_class'],
            total_fare=data['total_fare'],
            status='Confirmed'
        )

        for p in data.get('passengers', []):
            Passenger.objects.create(
                booking=booking,
                name=p['name'],
                age=p['age'],
                gender=p['gender'],
                seat_number=p['seat_number'],
                coach=p.get('coach', 'S1')
            )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_booking(request, pnr):
    try:
        booking = Booking.objects.get(pnr=pnr)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response(
            {'error': 'PNR not found'},
            status=status.HTTP_404_NOT_FOUND
        )