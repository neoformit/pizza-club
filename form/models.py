from django.db import models
import datetime

# Create your models here.
class Order(models.Model):
    date = models.DateField(("Date"), default=datetime.date.today)
    name = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self):
        return "%s - %s" % (self.date,self.name)

class Participant(models.Model):
    name = models.CharField(max_length=50)
    bsb = models.CharField(max_length=7)
    account = models.CharField(max_length=9)
    last_turn = models.DateField(("Date"), default=datetime.date.today)
    email = models.CharField(max_length=80)
    def __str__(self):
        return self.name