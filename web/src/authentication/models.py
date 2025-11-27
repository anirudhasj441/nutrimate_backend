from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class GoalChoices( models.TextChoices ):
    LOSE_WEIGHT = "LW", "Lose Weight"
    GAIN_MUSCLE = "GM", "Gain Muscle"
    MAINTAIN_WEIGHT = "MW", "Maintain Weight"
    IMPROVE_ENDURANCE = "IE", "Improve Endurance"
    FLEXIBILITY = "IF", "Increase Flexibility"
    FAT_LOSS = "FL", "Fat Loss"

class CustomUser( AbstractUser ):
    birth_date= models.DateField( null=True, blank=True )
    height = models.FloatField( null=True, blank=True )
    weight = models.FloatField( null=True, blank=True )
    goal = models.CharField( max_length=2, choices= GoalChoices.choices, 
            null=True, blank=True )
    
