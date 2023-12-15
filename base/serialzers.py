from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User
from .models import Hostel, Room, Reservation
class HostelSerializer(ModelSerializer):
    hostelManager = CharField(source = "manager.email",read_only=True)
    class Meta:
        model = Hostel
        fields = '__all__'
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class ReservationSerializer(ModelSerializer):
    hostel = CharField(source="room.hostel",read_only=True)
    roomNo = CharField(source="room.number",read_only=True)
    student = CharField(source = "user.email",read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'
