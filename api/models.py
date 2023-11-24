from django.db import models
from django.utils.translation import gettext_lazy as _

class ChatLog(models.Model):
    content = models.JSONField(_("log content"), null=True, blank=True)

    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('last modified'), auto_now=True)
    