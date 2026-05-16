import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Passenger
from .serializers import BookingSerializer
from trains.models import Train


def generate_pnr():
    return ''.join(random.choices(string.digits, k=10))


def _lock_seats(train, travel_class, passengers):
    """Add booked seats to train's booked_seats and seat_gender fields."""
    booked = list(train.booked_seats.get(travel_class, []))
    gender_map = dict(train.seat_gender.get(travel_class, {}))

    for p in passengers:
        seat_num = int(p['seat_number'])
        if seat_num not in booked:
            booked.append(seat_num)
        # Map gender: 'Male'/'M' → 'M', 'Female'/'F' → 'F'
        g = p.get('gender', 'M')
        gender_map[str(seat_num)] = 'M' if str(g).upper().startswith('M') else 'F'

    train.booked_seats[travel_class] = booked
    train.seat_gender[travel_class] = gender_map
    train.save()


def _unlock_seats(train, travel_class, passengers):
    """Remove seats from train's booked_seats and seat_gender when cancelled."""
    booked = list(train.booked_seats.get(travel_class, []))
    gender_map = dict(train.seat_gender.get(travel_class, {}))

    for p in passengers:
        seat_num = int(p.seat_number)
        if seat_num in booked:
            booked.remove(seat_num)
        gender_map.pop(str(seat_num), None)

    train.booked_seats[travel_class] = booked
    train.seat_gender[travel_class] = gender_map
    train.save()


@api_view(['POST'])
def create_booking(request):
    data = request.data
    pnr = generate_pnr()

    try:
        train = Train.objects.get(id=data['train_id'])

        booking = Booking.objects.create(
            pnr=pnr,
            train=train,
            journey_date=data['journey_date'],
            travel_class=data['travel_class'],
            total_fare=data['total_fare'],
            status='Confirmed'
        )

        passengers_data = data.get('passengers', [])
        for p in passengers_data:
            Passenger.objects.create(
                booking=booking,
                name=p['name'],
                age=p['age'],
                gender=p['gender'],
                seat_number=p['seat_number'],
                coach=p.get('coach', 'S1')
            )

        # Lock the seats on the Train record
        _lock_seats(train, data['travel_class'], passengers_data)

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Train.DoesNotExist:
        return Response({'error': 'Train not found'}, status=status.HTTP_404_NOT_FOUND)
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


@api_view(['POST'])
def cancel_booking(request, pnr):
    """Cancel a booking and unlock the seats for other users."""
    try:
        booking = Booking.objects.get(pnr=pnr)

        if booking.status == 'Cancelled':
            return Response({'error': 'Booking already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        # Unlock the seats on the Train record
        _unlock_seats(booking.train, booking.travel_class, booking.passengers.all())

        booking.status = 'Cancelled'
        booking.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    except Booking.DoesNotExist:
        return Response({'error': 'PNR not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
