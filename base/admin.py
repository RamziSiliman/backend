from django.contrib import admin
from .models import Hostel, Room, Reservation
# Register your models here.
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Reservation)
