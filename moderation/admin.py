from django.contrib import admin
from .models import ModerationRequest

# Register your models here.
@admin.register(ModerationRequest)
class ModerationRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "severity_score", "created_at"]

    list_filter = ["category", "created_at"]

    search_fields = ["content", "reasoning"]

    readonly_fields = ["created_at"]