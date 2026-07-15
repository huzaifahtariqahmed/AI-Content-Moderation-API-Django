from doctest import OutputChecker
from unicodedata import category
from unittest import result
from django.shortcuts import render
import moderation
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ModerationRequest
from .serializers import (
    ModerationRequestSerializer,
    ModerationSubmitSerializer,
    BulkModerationSubmitSerializer,
)
from .services import moderate_content

# Create your views here.
class ModerationViewSet(viewsets.ModelViewSet):
    serializer_class = ModerationRequestSerializer

    filterset_fields = ["category"]

    ordering_fields = ["-created_at", "severity_score"]

    ordering = ["-created_at"]

    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return ModerationRequest.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        submit_serializer = ModerationSubmitSerializer(data=request.data)

        submit_serializer.is_valid(raise_exception=True)

        content = submit_serializer.validated_data["content"]

        result = moderate_content(content)

        moderation = ModerationRequest.objects.create(
            user=request.user,
            content=content,
            category=result["category"],
            severity_score =result["severity_score"],
            reasoning=result["reasoning"]
        )

        output_serializer = ModerationRequestSerializer(moderation)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        serializer = BulkModerationSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = []
        for content in serializer.validated_data["contents"]:
            result = moderate_content(content)
            moderation = ModerationRequest.objects.create(
                user=request.user,
                content=content,
                category=result["category"],
                severity_score=result["severity_score"],
                reasoning=result["reasoning"],
            )
            results.append(moderation)
        output_serializer = ModerationRequestSerializer(results, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)