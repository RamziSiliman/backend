from django.db import models
from django.contrib.auth.models import User



class Hostel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    photo = models.FileField(upload_to='static/hostels')
    manager = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager")
    description = models.TextField(default="blank") 
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    capacity = models.DecimalField(decimal_places=0, max_digits=1)
    price = models.DecimalField(decimal_places=0, max_digits=10000000)
    photo = models.FileField(upload_to='static/rooms')    
    occupants = models.ManyToManyField(User, related_name="occupants", null=True, blank=True)
    class Meta:
        ordering=['-id']
    def __str__(self):
        return self.number 

class Reservation(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=0, max_digits=100000000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)    

    def __str__(self):
        return str(self.date)  




