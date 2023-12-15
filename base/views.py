from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Hostel, Room, Reservation
from django.contrib.auth.models import User
from .serialzers import HostelSerializer, RoomSerializer, UserSerializer, ReservationSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['groups'] = [group.name for group in user.groups.all()] 

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




@api_view(['GET', 'POST'])
def getUsers(request,pk):
    users = User.objects.all()

    # try:
    if request.method == "POST":
            
            

            # assign a user to a group
         
            if pk== "student":
                group = Group.objects.get(name="student")
            elif pk == "manager":
                group = Group.objects.get(name="manager")
            elif pk == "dean":
                group = Group.objects.get(name="dean")

            # creating a new user in the db
            user=UserSerializer(data=request.data)
            if user.is_valid():
                userSave = user.save(password = make_password(request.data['password']))
                group.user_set.add(userSave.id)
                return Response(user.data, status=status.HTTP_201_CREATED)
            
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    converted = UserSerializer(users, many=True)
    return Response(converted.data)
# functional based view for retrieving all hostels from the database 
@api_view(['GET','POST'])
def Hostels(request):
    try:
        if request.method == "POST":
                converted = HostelSerializer(data=request.data)
                if converted.is_valid():
                    converted.save()
                return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:    
        hostels = Hostel.objects.all()
        converted = HostelSerializer(hostels, many=True)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def getHostel(request,pk):
    try:
        hostel = Hostel.objects.get(id=pk)
        converted = HostelSerializer(hostel)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# functional based view for retrieving all rooms in a specified hostel from the database     
@api_view(['GET','POST'])
def hostelRooms(request, pk):
    try:
       if request.method== 'POST':
          Serialized=RoomSerializer(data=request.data)
          if Serialized.is_valid():
            Serialized.save()
            return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        hostel = Hostel.objects.get(id=pk)
        rooms = hostel.room_set.all()
        converted = RoomSerializer(rooms, many=True)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# function based view for making a reservation  and retrieving previous reservations
@api_view(['GET', 'POST'])
def reservation(request, pk):
    # POST 
    if request.method == 'POST':
        try:
            converted = ReservationSerializer(data = request.data)
            if converted.is_valid():
                converted.save()
                return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_304_NOT_MODIFIED)    

    # GET 
    try:
        user = User.objects.get(id=pk)
        reservations = user.reservation_set.all()
        converted = ReservationSerializer(reservations, many=True)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def myHostel(request, pk):
    try: 
        hostel = Hostel.objects.get(manager = pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    converted = HostelSerializer(hostel)
    return Response(converted.data)
        

@api_view(['GET','POST'])
def getReservations(request, pk):
    # try:
    #     try:
        if request.method == 'POST':
                converted = ReservationSerializer(data=request.data)
                if converted.is_valid():
                    
                    room = Room.objects.get(id = int(request.data['room']))
                    try:
                        resident = room.occupants.all().get(id=int(request.data['user']))
                    except:  
                        resident = 0  
                    if resident == 0:
                        if room.occupants.all().count() < 10:
                            Reservation.objects.create(
                                hostel = Hostel.objects.get(id=pk),
                                room = Room.objects.get(id = int(request.data['room'])),
                                user = User.objects.get(id = int(request.data['user'])),
                                amount = request.data['amount']
                            )
                            room.occupants.add(int(request.data['user']))
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_226_IM_USED)
                        
                    else:
                        return Response(status=status.HTTP_304_NOT_MODIFIED)    
        # except:
        #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)        
        hostel = Hostel.objects.get(id=pk)
        reservations = hostel.reservation_set.all()
        converted = ReservationSerializer(reservations, many=True)
        return Response(converted.data)
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
# @permission_classes([IsAuthenticated])
def updateHostel(request, pk):
    try:
        hostel = Hostel.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        Updated = HostelSerializer(hostel, data=request.data, partial=True)
        if Updated.is_valid():
            Updated.save()
            # send_mail("Account approval", f"your  hostel ({hostel.name}) has been approved successfully on the Hostel Booking System","kigongovincent81@gmail.com", [hostel.manager.email])
            return Response(Updated.data, status=status.HTTP_202_ACCEPTED)
        return Response(Updated.errors, status=status.HTTP_400_BAD_REQUEST)

    Updated = HostelSerializer(hostel)
    return Response(Updated.data)
@api_view(['GET', 'PATCH'])
# @permission_classes([IsAuthenticated])
def updateRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        Updated = RoomSerializer(room, data=request.data, partial=True)
        if Updated.is_valid():
            Updated.save()
            # send_mail("Account approval", f"your  hostel ({hostel.name}) has been approved successfully on the Hostel Booking System","kigongovincent81@gmail.com", [hostel.manager.email])
            return Response(Updated.data, status=status.HTTP_202_ACCEPTED)
        return Response(Updated.errors, status=status.HTTP_400_BAD_REQUEST)

    Updated = RoomSerializer(room)
    return Response(Updated.data)

