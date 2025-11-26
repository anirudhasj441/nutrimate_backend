"""
@file serializers.py
@brief Serializer definitions for the User model.
@details This file contains the serializer for the CustomUser model, which 
    field definitions, validation logic, and user creation logic.
"""


from django.contrib.auth.models import Group, User
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        """
        @brief Meta configuration for the userSerializer.
        @details Specifies the model to be serialized and the fields to include. 
                 Also defines additional keyword arguments for certain fields.
        """
        # @brief The model being serialized.
        model = User

        # @brief The fields to include in the serialized output.
        fields = [
            'username', 
            'email', 
            'password', 
            'first_name', 
            'last_name',
            'birth_date',
            'height',
            'weight',
            'goal'
        ]

        # @brief Additional keyword arguments for serializer fields.
        extra_kwargs = {'password': {'write_only': True}}

        # --------------------------------------------------------------
    # @brief Validates the input data for the serializer.
    # @details Ensures that all required fields are present unless it's a partial update.
    # @param data The input data to validate.
    # @return The validated data if all required fields are present.
    # @throws ValidationError if any required field is missing.
    # --------------------------------------------------------------
    def validate(self, data):
        """
        @brief Validates the input data for the serializer.
        @details Ensures that all required fields are present unless it's a partial update.
        @param data The input data to validate.
        @return The validated data if all required fields are present.
        @throws ValidationError if any required field is missing.
        """
        required_fields = [
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'birth_date',
            'height',
            'weight',
            'goal'
        ]
        
        # If this is a partial update, skip validation for missing required fields.
        if self.partial:
            return data
        
        # Check for each required field in the data.
        for field in required_fields:
            if field not in data.keys():
                raise ValidationError({field: f"{field} is required"})
            
        return data

    # --------------------------------------------------------------
    # @brief Creates a new CustomUser instance.
    # @details Handles the creation of a new user using the validated data.
    # @param validated_data The validated data for creating the user.
    # @return The newly created CustomUser instance.
    # --------------------------------------------------------------
    def create(self, validated_data):
        """
        @brief Creates a new CustomUser instance.
        @details Handles the creation of a new user using the validated data.
        @param validated_data The validated data for creating the user.
        @return The newly created CustomUser instance.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            birth_date=validated_data["birth_date"],
            height=validated_data["height"],
            weight=validated_data["weight"],
            goal=validated_data["goal"]
        )
        return user