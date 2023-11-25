from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
UserModel = get_user_model()


class ChatSession(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(_("session title"), max_length=300, null=True, default="New Session")
    content = models.JSONField(_("log content"), null=True, blank=True)

    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('last modified'), auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if not self.content:
            cnt = open((settings.BASE_DIR/'user/context.txt'), 'r').read().format(self.user.full_name)
            self.content = {'messages': [{'role': 'system','content': cnt}]}
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Chat session for {self.user.full_name}, created {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}."