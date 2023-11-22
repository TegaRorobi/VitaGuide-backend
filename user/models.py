
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from .manager import UserManager



class User(AbstractUser):

    username = models.CharField(
        _("username"),
        unique=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        help_text=_("Not required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"unique": _("A user with that username already exists."),},
        null=True, blank=True
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150, null=True, blank=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    chat_logs = models.JSONField(_("chat logs"), null=True, blank=True)

    groups = None
    is_staff = None 
    is_active = None 
    is_superuser = None
    user_permissions = None
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs) -> None:
        if not self.chat_logs:
            self.chat_logs = {
                'messages': [{
                    'role': 'system',
                    'content': open((settings.BASE_DIR/'user/context.txt'), 'r').read()
                }]
            }
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} ({self.email})".strip()