from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "phone_number",
        )

        read_only_fields = (
            "id",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "phone_number",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data) -> User:
        user = User.objects.create_user(**validate_data)
        return user
