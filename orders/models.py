from django.db import models

# Create your models here.


class Pizza(models.Model):
    SM = 'Small'
    LG = 'Large'
    SIZE = [(SM, 'Small'), (LG, 'Large')]

    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    TOPPINGS_NUMBER = [(ZERO, 0),
                       (ONE, 1),
                       (TWO, 2),
                       (THREE, 3),
                       (FIVE, 5)]

    name = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    price = models.FloatField()
    size = models.CharField(
        max_length=6, choices=SIZE, default=SM)
    toppings_number = models.IntegerField(
        choices=TOPPINGS_NUMBER, default=ZERO)

    def __str__(self):
          return f"{self.name} {self.size} {self.type} with {self.toppings_number} toppings costs {self.price}"

class Topping(models.Model):
  name = models.CharField(max_length=64)
  
  def __str__(self):
    return f"{self.name} is a topping name"
