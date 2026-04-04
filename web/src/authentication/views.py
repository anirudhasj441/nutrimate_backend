"""
@file views.py
@brief API views for user authentication and registration.

This module contains API views for user authentication and registration using 
Django Rest Framework. It includes views for checking username availability, 
user registration, and user login. JWT tokens are utilized for authentication, 
and user data is managed using Django's built-in User model.

@module
"""
from authentication.serializers import UserSerializer, FitnessTrackerSerializer
from django.contrib.auth.models import Group, User
from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .models import FitnessTracker

User = get_user_model()

def getUserToken(user):
    """
    @brief Generates JWT tokens for the given user.

    This function creates and returns refresh and access tokens using the 
    `RefreshToken`
    class from the `rest_framework_simplejwt` package.

    @param user The user object for whom tokens are generated.
    @return A dictionary containing 'refresh' and 'access' tokens as strings.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class GetUser( APIView ):
    """
    @brief API view to get the authenticated user's information.

    This view handles GET requests and returns the currently authenticated 
    user's data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        @brief Handles GET requests to return the authenticated user's data.

        @param request The HTTP request object.
        @return Response A Response object containing the user's data.
        """
        serializer = UserSerializer(request.user)
        
        return Response({
            "payload": serializer.data
        }, status=status.HTTP_200_OK)


class LoginUser(APIView):
    """
    @brief API view to handle user login.

    This view processes POST requests for user authentication. It validates the 
    credentials, generates
    JWT tokens upon successful login, and returns them in the response.
    """

    def post(self, request):
        """
        @brief Handles POST requests for user login.

        @param request The HTTP request object containing username and password.
        @return Response A Response object with login status, JWT tokens, and 
            user data upon success.
        """
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {
                    "detail": "No active account found with the given \
                        credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = getUserToken(user)
        
        response = Response()

        serializer = UserSerializer(User.objects.get(username=user))

        response.data = {
            'message': 'Login successful',
            'refresh': tokens["refresh"],
            'access': tokens["access"],
            'user': serializer.data
        }

        response.status = status.HTTP_200_OK

        return response

class SignUpUser(APIView):
    """
    @brief API view to handle user registration.

    This view handles POST requests for creating a new user. It validates the input data using
    a serializer, creates a user, and generates JWT tokens.
    """

    def post(self, request):
        """
        @brief Handles POST requests for user registration.

        @param request The HTTP request object containing user registration data.
        @return Response A Response object with registration status and JWT tokens upon success.
        """
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'error': serializer.errors,
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'payload': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
    

class FitnessTrackerViewSet( APIView ):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = FitnessTrackerSerializer( FitnessTracker.objects.filter(user=request.user, date=timezone.now().date()), many=True )

        return Response({
            "payload": serializer.data,
            "message": "Data retrieved successfully!"
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        serializer = FitnessTrackerSerializer( data={
            "user": request.user.pk,
            "date": timezone.now().date(),
            "calories_consumed": data.get("calories_consumed", 0),
            "steps": data.get("steps", 0),
            "water_intake": data.get("water_intake", 0)
        } )

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'error': serializer.errors,
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "payload": serializer.data,
            "message": "Data saved successfully!"
        }, status=status.HTTP_201_CREATED)
    
    def patch(self, request):
        tracker = FitnessTracker.objects.get( user=request.user, date=timezone.now().date() )

        if not tracker:
            return Response({
                'status': 404,
                'message': "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)
        


        serializer = FitnessTrackerSerializer( tracker, data={
            "user": request.user.pk,
            "date": timezone.now().date(),
            "calories_consumed": request.data.get("calories_consumed", 0),
            "steps": request.data.get("steps", 0),
            "water_intake": request.data.get("water_intake", 0)
        }, partial=True )

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'error': serializer.errors,
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save( )

        return Response({
            "payload": serializer.data,
            "message": "Data partially updated successfully!"
        }, status=status.HTTP_200_OK)
    
    def delete(self, request):
        fitness_tracker = FitnessTracker.objects.filter( user=request.user, date=timezone.now().date() ).first()

        if not fitness_tracker:
            return Response({
                'status': 404,
                'message': "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

        fitness_tracker.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)