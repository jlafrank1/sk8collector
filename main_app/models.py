from django.db import models
from django.urls import reverse
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User


EQUIPMENT = (
    ('B', 'Bearings'),
    ('T', 'Toe stops'),
    ('P', 'Plates'),
    ('W', 'Wheels'),
    ('S', 'Slider blocks'),
    ('C', 'Cushions'),
    ('O', 'Other')
)

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    has_ramps = models.BooleanField()
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'pk': self.id})

class Skate(models.Model):
    nickname = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    plates = models.CharField(max_length=100)
    stops = models.CharField(max_length=100)
    wheels = models.CharField(max_length=100)
    bearings = models.CharField(max_length=100)
    cushions = models.CharField(max_length=100)
    slides = models.CharField(max_length=100)
    places = models.ManyToManyField(Place)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('detail', kwargs={'skate_id': self.id})

    def needs_maintenace(self):
        latest_entry = self.maintenance_set.filter(date__isnull=False).latest('date').date
        today = date.today()
        time_since_maintenance = today - latest_entry
        time_since_maintenance_days = time_since_maintenance.days
        # THANK YOU JACKSON REEVES FOR HELPING ME WITH THIS CODE I WANT TO BE LIKE YOU WHEN I GROW UP
        if time_since_maintenance_days < 28:
            return True
        else:
            return False


class Maintenance(models.Model):
    date = models.DateField('maintenance date')
    equipment = models.CharField(
        max_length=1,
        choices=EQUIPMENT,
        default=EQUIPMENT[0][0]
        )
    entry = models.CharField(max_length=250)

    skate = models.ForeignKey(Skate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_equipment_display()} on {self.date}"

    class Meta:
        ordering =['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    skate = models.ForeignKey(Skate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for skate_id: {self.skate_id} @{self.url}"



# class Skate:
#     def __init__(self, nickname, brand, style, color, plates, stops, wheels, bearings, cushions, slides):
#         self.nickname = nickname
#         self.brand = brand
#         self.style = style
#         self.color = color
#         self.plates = plates
#         self.stops = stops
#         self.wheels = wheels
#         self.bearings = bearings
#         self.cushions = cushions
#         self.slides = slides

# skates = [
#     Skate('Antiks', 'Antik', 'hightop', 'red and black', 'Sunlite', 'Bont Toe-Goe', 'Moxi Gummy 78a', 'unknown', 'unknown', 'Wildbones'),
#     Skate('Lollies', 'Moxi', 'Lolly', 'black', 'stock', 'Gumball long stem', 'Moxi Gummy 78a', 'unknown', 'stock', 'None'),
#     Skate('Bonts', 'Bont', 'Custom', 'white and black', 'Athena', 'Bont Toe-Goe', 'FXX 88a', 'micro', 'unknown', 'none')
# ]
