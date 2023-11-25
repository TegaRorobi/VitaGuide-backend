from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
UserModel = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='chat_sessions')
    content = models.JSONField(_("log content"), null=True, blank=True)

    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('last modified'), auto_now=True)
    
    def __str__(self) -> str:
        return f"Chat session for {self.user.full_name}, created {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}."