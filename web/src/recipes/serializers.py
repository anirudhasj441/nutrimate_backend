"""
@file serializers.py
@brief Serializer definitions for the User model.
@details This file contains the serializer for the CustomUser model, which 
    field definitions, validation logic, and user creation logic.
"""
from recipes.models import Recipe, Ingredient, RecipeIngredient

from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from django.contrib.auth import get_user_model

User = get_user_model()

class IngredientSerializer(ModelSerializer):
    class Meta:
        """
        @brief Meta configuration for the IngredientSerializer.
        @details Specifies the model to be serialized and the fields to include.
        """
        # @brief The model being serialized.
        model = Ingredient  # Replace with actual Ingredient model when available

        # @brief The fields to include in the serialized output.
        fields = [
            'name',
            'calories',
            'protein',
            'fat',
            'carbohydrates'
        ]

    def validate(self, data):
        """
        @brief Validates the input data for the serializer.
        @details Ensures that all required fields are present unless it's a partial update.
        @param data The input data to validate.
        @return The validated data if all required fields are present.
        @throws ValidationError if any required field is missing.
        """
        required_fields = [
            'name'
        ]

        for field in required_fields:
            if field not in data and not self.partial:
                raise ValidationError({field: f"{field} is required."})

        return data
    
# ---------------- RecipeIngredient Serializer ----------------
class RecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'ingredient', 'quantity', 'unit']

        extra_kwargs = { 'recipe': { 'write_only': True }, 'ingredient': { 'write_only': True } }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Replace ingredient ID with full ingredient object
        data['ingredient'] = IngredientSerializer(instance.ingredient).data

        return data
class RecipeSerializer(ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set',
        # write_only=True,
        read_only=True
    )

    class Meta:
        """
        @brief Meta configuration for the RecipeSerializer.
        @details Specifies the model to be serialized and the fields to include.
        """
        # @brief The model being serialized.
        model = Recipe  # Replace with actual Recipe model when available

        # @brief The fields to include in the serialized output.
        fields = [
            'id',
            'title',
            'description',
            'instructions',
            'recipe_ingredients',
            'category',
            'prep_time',
            'cook_time',
            'servings',
            'calories',
            'protein',
            'fat',
            'carbohydrates',
            'img',
            'created_at',
            'updated_at'
        ]

    def validate(self, data):
        """
        @brief Validates the input data for the serializer.
        @details Ensures that all required fields are present unless it's a partial update.
        @param data The input data to validate.
        @return The validated data if all required fields are present.
        @throws ValidationError if any required field is missing.
        """
        required_fields = [
            'title',
            'description',
            'instructions'
        ]

        for field in required_fields:
            if field not in data and not self.partial:
                raise ValidationError({field: f"{field} is required."})

        return data
    
    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients_data')
    #     recipe = Recipe.objects.create(**validated_data)

    #     for item in ingredients:
    #         Ingredient.objects.create(recipe=recipe, **item)

    #     return recipe
    
    # def update(self, instance, validated_data):
    #     ingredients = validated_data.pop('ingredients_data', None)

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     if ingredients is not None:
    #         instance.ingredients.all().delete()
    #         for item in ingredients:
    #             Ingredient.objects.create(recipe=instance, **item)

    #     return instance


