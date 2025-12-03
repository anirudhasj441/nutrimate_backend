from recipes.models import Recipe, Ingredient, RecipeIngredient
from recipes.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
# Create your views here.


User = get_user_model()

class RecipeListView( APIView ):
    permission_classes = [ IsAuthenticated ]

    def get( self, request, recipe_id=None ):
        if recipe_id:
            try:
                recipe = Recipe.objects.get( id=recipe_id )
                serializer = RecipeSerializer( recipe )
                return Response( { "recipe": serializer.data } )
            except Recipe.DoesNotExist:
                return Response( { "error": "Recipe not found." }, status=404 )

        recipes = Recipe.objects.all()
        if recipes.exists():
            serializer = RecipeSerializer( recipes, many=True )
            return Response( { "recipes": serializer.data } )

        return Response( { "recipes": [] } )
    
    def post( self, request ):
        data = request.data

        recipe_serializer = RecipeSerializer(data={
            "title": data["title"],
            "description": data.get("description", ""),
            "instructions": data.get("instructions", ""),
            "category": data.get("category"),
            "prep_time": data.get("prep_time"),
            "cook_time": data.get("cook_time"),
            "servings": data.get("servings"),
            "calories": data.get("calories"),
            "protein": data.get("protein"),
            "fat": data.get("fat"),
            "carbohydrates": data.get("carbohydrates"),
            "img": data.get("img")
        })

        if not recipe_serializer.is_valid( raise_exception=True ):
            return Response({
                "error": "Invalid recipe data.", 
                "details": recipe_serializer.errors 
            }, status=400 )

        recipe = recipe_serializer.save()
        
        ingredients = data.get( "recipe_ingredients", [] )

        for ingredient in ingredients:
            ingredient_obj = Ingredient.objects.filter( name=ingredient.get( "ingredient", {} ).get( "name" ) ).first()

            if not ingredient_obj:
                ingredientSerializer = IngredientSerializer( data=ingredient.get( "ingredient", {} ))
                if not ingredientSerializer.is_valid():
                    return Response({
                        "error": "Invalid ingredient data.", 
                        "details": ingredientSerializer.errors 
                    }, status=400 )
                
                ingredient_obj = ingredientSerializer.save()
            
            recipeInerdientSerializer = RecipeIngredientSerializer( data = {
                "recipe": recipe.pk,
                "ingredient": ingredient_obj.pk,
                "quantity": ingredient.get( "quantity" ),
                "unit": ingredient.get( "unit" )
            })

            if not recipeInerdientSerializer.is_valid( raise_exception=True ):
                return Response({
                    "error": "Invalid recipe ingredient data.", 
                    "details": recipeInerdientSerializer.errors 
                }, status=400 )
            
            recipeInerdientSerializer.save()

        return Response(
            {
                "message": "Recipe created successfully.",
                "payload": RecipeSerializer( recipe ).data
            },
            status=status.HTTP_201_CREATED
        )
            
        





