from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('<str:pnr>/', views.get_booking, name='get_booking'),
    path('<str:pnr>/cancel/', views.cancel_booking, name='cancel_booking'),
]
