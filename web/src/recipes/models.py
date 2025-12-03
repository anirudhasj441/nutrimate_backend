from django.db import models

# Create your models here.
class CategoryChoices( models.TextChoices ):
    BREAKFAST = "BF", "Breakfast"
    LUNCH = "LU", "Lunch"
    DINNER = "DI", "Dinner"
    SNACK = "SN", "Snack"
    DESSERT = "DE", "Dessert"
    BEVERAGE = "BE", "Beverage"

class UnitChoices( models.TextChoices ):
    GRAM = "g", "Gram"
    KILOGRAM = "kg", "Kilogram"
    MILLILITER = "ml", "Milliliter"
    LITER = "l", "Liter"
    CUP = "cup", "Cup"
    TABLESPOON = "tbsp", "Tablespoon"
    TEASPOON = "tsp", "Teaspoon"
    PIECE = "pc", "Piece"

class Recipe( models.Model ):
    title = models.CharField( max_length=200 )
    description = models.TextField()
    instructions = models.TextField()
    category = models.CharField( max_length=100, choices=CategoryChoices.choices, null=True, blank=True )    
    ingredient = models.ManyToManyField( 'Ingredient', related_name='recipes', through='RecipeIngredient', blank=True )
    prep_time = models.IntegerField( null=True, blank=True )  # in minutes
    cook_time = models.IntegerField( null=True, blank=True )  # in minutes
    servings = models.IntegerField( null=True, blank=True )
    calories = models.IntegerField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)  # in grams
    fat = models.FloatField(null=True, blank=True)      # in grams
    carbohydrates = models.FloatField(null=True, blank=True)  # in grams
    img = models.URLField( null=True, blank=True )
    created_at = models.DateTimeField( auto_now_add=True )
    updated_at = models.DateTimeField( auto_now=True )
    
    def __str__( self ):
        return self.title
    
class Ingredient( models.Model ):
    name = models.CharField( max_length=200 )
    calories = models.IntegerField( null=True, blank=True )  # per 100g
    protein = models.FloatField( null=True, blank=True )    # per 100g
    fat = models.FloatField( null=True, blank=True )        # per 100g
    carbohydrates = models.FloatField( null=True, blank=True )  # per 100g
    def __str__( self ):
        return self.name
    
class RecipeIngredient( models.Model ):
    recipe = models.ForeignKey( Recipe, on_delete=models.CASCADE )
    ingredient = models.ForeignKey( Ingredient, on_delete=models.CASCADE )
    quantity = models.FloatField()
    unit = models.CharField( max_length=10, choices=UnitChoices.choices )
    
    def __str__( self ):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.title}"
    
    class Meta:
        db_table = 'recipe_recipeingredient'
