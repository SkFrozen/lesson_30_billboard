from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True, slug_field="username", read_only=True
    )

    class Meta:
        model = Event
        fields = ("title", "meeting_time", "description", "users")


class EventSubscribeSerializer(serializers.ModelSerializer):
    users = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = ("users",)

    def update(self, instance, validated_data):
        instance.users.add(validated_data["users"])
        return instance
