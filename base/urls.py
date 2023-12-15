from . import views
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('hostels/', views.Hostels, name = "hostels"),
    path('register/<str:pk>', views.getUsers),
    path('rooms/<str:pk>', views.hostelRooms, name = "hostelsRooms"),
    path('hostel/<str:pk>', views.getHostel, name = "hostel"),
    path('myhostel/<str:pk>', views.myHostel, name = "myhostel"),
    path('updateroom/<str:pk>', views.updateRoom),
    path('reservations/<str:pk>', views.reservation, name = "reservations"),
    path('update/<str:pk>', views.updateHostel),
    path('hostelReservations/<str:pk>', views.getReservations, name = "hostel-reservations"),
]