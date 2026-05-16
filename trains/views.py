from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Train
from .serializers import TrainSerializer

class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

@api_view(['GET'])
def search_trains(request):
    from_station = request.query_params.get('from', '')
    to_station = request.query_params.get('to', '')
    trains = Train.objects.filter(
        from_station__icontains=from_station,
        to_station__icontains=to_station
    )
    serializer = TrainSerializer(trains, many=True)
    return Response(serializer.data)