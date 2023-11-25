
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from .manager import UserManager
from api.models import ChatLog



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
    full_name = models.CharField(_("full name"), max_length=300)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    chat_log = models.OneToOneField(ChatLog, related_name='user', on_delete=models.SET_NULL, null=True)

    first_name = None 
    last_name = None
    groups = None
    user_permissions = None
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs) -> None:
        if not self.chat_log:
            cnt = open((settings.BASE_DIR/'user/context.txt'), 'r').read().format(self.first_name, self.last_name)
            self.chat_log = ChatLog.objects.create(content={'messages': [{'role': 'system','content': cnt}]})
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} ({self.email})".strip()