from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'trains', views.TrainViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search_trains, name='search_trains'),
]