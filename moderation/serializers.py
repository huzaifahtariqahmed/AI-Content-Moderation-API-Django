from typing import ReadOnly
from rest_framework import serializers
from .models import ModerationRequest

class ModerationRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ModerationRequest

        fields = ["id", "user", "content", "category", "severity_score", "reasoning", "created_at"]

        read_only_fields = ["id", "user", "category", "severity_score", "reasoning", "created_at"]

class ModerationSubmitSerializer(serializers.Serializer):
    content = serializers.CharField(min_length=1, max_length=5000)

class BulkModerationSubmitSerializer(serializers.Serializer):
    contents = serializers.ListField(
        child=serializers.CharField(
            min_length=1,
            max_length=5000,
        ),
        min_length=1,
        max_length=10,
    )