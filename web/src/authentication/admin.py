from authentication.models import CustomUser
from django.contrib import admin
from django.db import models
from django.forms import NumberInput
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register( CustomUser )
class CustomUserAdmin( UserAdmin ):
    fieldsets = UserAdmin.fieldsets + (
        ( "Additional Info", {"fields": ( 
            "birth_date", 
            "height", 
            "weight", 
            "goal" 
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ( "Additional Info", {"fields": ( 
            "birth_date", 
            "height", 
            "weight", 
            "goal" 
        )}),
    )

    formfield_overrides = {
        models.FloatField: {'widget': NumberInput(attrs={'step': '0.01'})},
    }


