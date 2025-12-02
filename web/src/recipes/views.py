from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

from django.shortcuts import render
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
    

