from django.contrib.auth.models import User
from .models import Recipe , Rating , Shopping
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields='__all__'

class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shopping
        fields='__all__'