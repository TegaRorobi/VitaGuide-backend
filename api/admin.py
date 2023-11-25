from django.contrib import admin
from .models import ChatSession


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    model = ChatSession
    list_display = 'user', 'title', 'created_at', 'updated_at'
