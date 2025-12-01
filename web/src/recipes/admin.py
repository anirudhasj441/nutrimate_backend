from recipes.models import Recipe, Ingredient, RecipeIngredient
from django.contrib import admin

# Register your models here.

class RecipeIngredientInline( admin.TabularInline ):
    model = RecipeIngredient
    autocomplete_fields = ( 'ingredient', )
    extra = 1

@admin.register( Ingredient )
class IngredientAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'calories', 'protein', 'fat', 'carbohydrates', )
    search_fields = ( 'name', )

@admin.register( Recipe )
class RecipeAdmin( admin.ModelAdmin ):
    inlines = [ RecipeIngredientInline, ]
    list_display = ( 'title', 'category', 'prep_time', 'cook_time', 'servings', 'calories', )
    # filter_horizontal = ( 'Ingredient', )
    search_fields = ( 'title', )

@admin.register( RecipeIngredient )
class RecipeIngredientAdmin( admin.ModelAdmin ):
    list_display = ( 'recipe', 'ingredient', 'quantity', 'unit', )
    search_fields = ( 'recipe__title', 'ingredient__name', )