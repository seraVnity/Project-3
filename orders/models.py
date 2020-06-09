from django.db import models

# Create your models here.
class Pizzas(model.Models):
  name = models.CharField(max_length=64)
  size = models.CharField(max_length=64)
  type = models.CharField(max_length=64)
  price = models.IntegerField()
  size = models.CharField( max_length=2, choices = Size.TextChioces, default=Size.small)
  # toppings_number = models
  
  class Size(models.TextChoices):
    small = 'sm'
    large = 'lg'
  # class Toppings_Num(models.IntegerChoices):
