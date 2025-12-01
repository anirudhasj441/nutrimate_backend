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

    def get( self, request ):
        recipes = Recipe.objects.all()
        if recipes.exists():
            serializer = RecipeSerializer( recipes, many=True )
            return Response( { "recipes": serializer.data } )

        return Response( { "recipes": [] } )
