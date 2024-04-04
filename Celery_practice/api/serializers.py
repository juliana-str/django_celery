from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from orders.models import Order
from users.models import User


class UserGetSerializer(serializers.ModelSerializer):
    """Serializer for model User."""

    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name")


class UserPostSerializer(UserCreateSerializer):
    """Serializer for model User, create."""
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "password", "first_name")


class OrderGetSerializer(serializers.ModelSerializer):
    """Serializer for model Order."""

    class Meta:
        model = Order
        fields = '__all__'


class OrderPostSerializer(serializers.ModelSerializer):
    """Serializer for model Order, create."""

    class Meta:
        model = Order
        fields = '__all__'
