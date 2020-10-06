from django.db import models


class Beverage(models.Model):
    name = models.CharField(max_length=32)
    amount = models.IntegerField()
    alcoholic = models.BooleanField()

    def __str__(self):
        return self.name


class Snack(models.Model):
    name = models.CharField(max_length=32)
    amount = models.IntegerField()
    vegan = models.BooleanField()

    def __str__(self):
        return self.name
